from fastapi import APIRouter , Depends , status , HTTPException ,UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy import insert
from sqlalchemy.orm import Session
from app.config.database import get_session
from app.schemas.Foods import FoodRegister , FoodModify
from app.responses.foods import FoodResponse , FoodImageUpdate
from app.services.cuisine import create_cuisine , modify_cuisine , fetch_cuisine_detail , delete_cuisine
from app.models.user import Foods , Restaurants , t_foodcats
from typing import List ,Optional
import os
import uuid
import shutil

Food_router = APIRouter(
    prefix="/food",
    tags=["Foods"],
    responses={404: {"description": "Not found"}}
)
UPLOAD_DIRECTORY = "uploads/foods"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@Food_router.post("", status_code=status.HTTP_201_CREATED, response_model=FoodResponse)
def create_food(food: FoodRegister, session: Session = Depends(get_session)):
    # Ensure the restaurant exists
    restaurant = session.query(Restaurants).filter(Restaurants.id == food.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Create the new food item
    new_food = Foods(
        name=food.name,
        description=food.description,
        price=food.price,
        initial_stock=food.initial_stock,
        preparation_time=food.preparation_time,
        image_url=food.image_url,
        restaurant_id=food.restaurant_id
    )

    # Add food item to the session and commit
    session.add(new_food)
    session.commit()
    session.refresh(new_food)

    # Update categories if provided
    if food.categories:
        session.execute(t_foodcats.delete().where(t_foodcats.c.food_id == new_food.id))
        session.commit()

        category_relations = [{"food_id": new_food.id, "category_id": cat_id} for cat_id in food.categories]
        session.execute(insert(t_foodcats).values(category_relations))
        session.commit()

    # Return the newly created food item
    return new_food

@Food_router.put("/{food_id}", status_code=status.HTTP_200_OK, response_model=FoodResponse)
def modify_food(food_id: int, food: FoodRegister, session: Session = Depends(get_session)):
    # Ensure the restaurant exists
    restaurant = session.query(Restaurants).filter(Restaurants.id == food.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Find the existing food item
    existing_food = session.query(Foods).filter(Foods.id == food_id).first()
    if not existing_food:
        raise HTTPException(status_code=404, detail="Food not found")

    # Prevent modification of the restaurant_id (ensure it stays the same)
    if existing_food.restaurant_id != food.restaurant_id:
        raise HTTPException(status_code=400, detail="Cannot change the restaurant ID for this food item")

    # Update the food item attributes (excluding the restaurant_id)
    existing_food.name = food.name
    existing_food.description = food.description
    existing_food.price = food.price
    existing_food.initial_stock = food.initial_stock
    existing_food.preparation_time = food.preparation_time
    existing_food.image_url = food.image_url

    # Commit the changes to the session
    session.commit()
    session.refresh(existing_food)

    # Update categories if provided
    if food.categories is not None:
        # Remove the current category relations
        session.execute(t_foodcats.delete().where(t_foodcats.c.food_id == existing_food.id))
        session.commit()

        # Add the new category relations
        category_relations = [{"food_id": existing_food.id, "category_id": cat_id} for cat_id in food.categories]
        session.execute(insert(t_foodcats).values(category_relations))
        session.commit()

    # Return the modified food item
    return existing_food
@Food_router.delete("/{food_id}", status_code=status.HTTP_200_OK)
async def delete_food(food_id: int, session: Session = Depends(get_session)):
    # Check if the food exists in the database
    food = session.query(Foods).filter(Foods.id == food_id).first()

    if food is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with id {food_id} not found"
        )

    # Delete the food item from the database
    session.delete(food)
    session.commit()

    # Return a success status without any content
    return {"message": "Food item deleted successfully"}

@Food_router.get("/all/", response_model=List[FoodResponse])
async def get_foods(cuisine_id: Optional[int] = None, session: Session = Depends(get_session)):
    # Query to get all foods, optionally filtering by cuisine_id
    query = session.query(Foods)
    
    if cuisine_id:
        query = query.join(Restaurants).filter(Restaurants.cuisine_id == cuisine_id)

    foods = query.all()
    return foods

@Food_router.get("/food_restaurant_id/{restaurant_id}", response_model=List[FoodResponse])
async def get_foods_by_restaurant(
    restaurant_id: int,  # nicht optional – du brauchst diese ID
    session: Session = Depends(get_session)
):
    foods = session.query(Foods).filter(Foods.restaurant_id == restaurant_id).all()
    return foods


@Food_router.get("/foods/", response_model=List[FoodResponse])
async def get_foods_by_cuisine(cuisine_id: int, session: Session = Depends(get_session)):
    # Fetch foods by cuisine_id
    foods = session.query(Foods).join(Restaurants).filter(Restaurants.cuisine_id == cuisine_id).all()
    return foods


@Food_router.post("/upload&food/image/" )
async def upload_food_image(image: UploadFile =File(...)):
    upload_dir ="uploads/foods"
    os.makedirs(upload_dir , exist_ok= True) # Use exist_ok=True for robustness
    # Correct way to get file extension
    file_ext = image.filename.split('.')[-1]   

    # Optional: Basic validation to ensure there's an actual extension
    if not file_ext or '.' not in image.filename:
        # You might want to raise an HTTPException here or set a default
        # For example, raise HTTPException(status_code=400, detail="Invalid file: no extension found")
        file_ext = "bin" # Fallback to a generic binary extension if none is found or if it's just a filename with no dot.
                         # A better approach might be to validate allowed extensions here.

    filename = f"{uuid.uuid4()}.{file_ext}"
    filepath = os.path.join(upload_dir , filename)
    try:
        with open(filepath , "wb") as buffer :
            shutil.copyfileobj(image.file , buffer)
    except Exception as e:
        # Provide more specific error details in production
        raise HTTPException(status_code=500, detail=f"Failed to save image file: {e}")
    image_url=f"/uploads/foods/{filename}"
    return {"image_url": image_url}

   


@Food_router.patch("/{id}/image", status_code=status.HTTP_200_OK)
async def update_food_image(
    id: int,
    image_update: FoodImageUpdate, # Use the new Pydantic schema
    session: Session = Depends(get_session)
):
    """
    Updates only the image_url for a specific restaurant.
    """
    food = session.query(Foods).filter(Foods.id == id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    # Apply the update
    food.image_url = image_update.image_url
    session.add(food) # Or session.merge(restaurant) depending on your SQLAlchemy setup
    session.commit()
    session.refresh(food) # Refresh to get the latest state from DB
    # Return a success message or the updated image URL
    return {"message": "Food image updated successfully", "image_url": food.image_url}



