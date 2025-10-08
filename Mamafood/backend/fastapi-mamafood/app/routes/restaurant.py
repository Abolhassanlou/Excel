from fastapi import APIRouter, Depends, status, Query, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_session
from app.schemas.Restaurant import RestaurantModify , RestuarantRegister , RestaurantCreateForDB, RegisterUserRequest ,RestaurantRegistrationRequest
from app.schemas.user import RegisterUserRequest
from app.schemas.Address import RegisterAddress
from app.responses.restaurant import RestaurantResponse , RestaurantResponse2 , RestaurantImageUpdate
from app.responses.cuisine import CuisineResponse
from app.responses.address import AdressResponse
from app.services.restaurant import create_restaurant , modify_restaurant , fetch_restaurant_detail , delete_restaurant , filter_restaurants
from app.models.user import Restaurants , Cuisines ,Addresses , User
from app.config.security import  hash_password
from app.services.user import create_user_account
from fastapi.responses import JSONResponse
import os
import uuid
import shutil

Restaurant_router=APIRouter(
    prefix="/restaurant" ,
    tags=["restaurants"],
    responses={404: {"description" : "Not found "}}
)

UPLOAD_DIRECTORY = "uploads/restaurants"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@Restaurant_router.post("" , status_code=status.HTTP_201_CREATED , response_model=RestaurantResponse)
async def register_restaurant(data:RestuarantRegister, session: Session=Depends(get_session)):
    return await create_restaurant(data, session)


@Restaurant_router.post("/register-restaurant" , status_code=status.HTTP_201_CREATED , response_model=RestaurantResponse)
async def register_restaurant2(
    data: RestaurantRegistrationRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    # Create user with email activation and role=1 (restaurant)
    new_user = await create_user_account(data.user, session, background_tasks, role=1)
    # Create address
    new_address = Addresses(
        street=data.address.street,
        city=data.address.city,
        postal_code=data.address.postal_code,
        flat_number=data.address.flat_number,
        door_number=data.address.door_number,
        google_maps_link=data.address.google_maps_link
    )
    session.add(new_address)
    session.flush()  # To get new_address.id
    # Prepare restaurant data with user and address IDs
    restaurant_data_for_db = RestaurantCreateForDB(
        user_id=new_user.id,
        address_id=new_address.id,
        cuisine_id=data.restaurant.cuisine_id,
        restaurant_name=data.restaurant.restaurant_name,
        tel_number=data.restaurant.tel_number,
        description=data.restaurant.description,
        pickup_time=data.restaurant.pickup_time,
        image_url=data.restaurant.image_url

    )

    # Create restaurant in DB
    new_restaurant = await create_restaurant(restaurant_data_for_db, session)
    return new_restaurant

@Restaurant_router.get("/{id}" , response_model=RestaurantResponse2)
async def get_by_id(id:int , session:Session=Depends(get_session)):
    return await fetch_restaurant_detail (id , session)


@Restaurant_router.get("/user_id/{id}")
async def get_by_user_id(id: int, session: Session = Depends(get_session)):
    restaurant = session.query(Restaurants).filter(Restaurants.user_id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"restaurant_id": restaurant.id}


@Restaurant_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=RestaurantResponse)
async def update_restaurant(id , data:RestaurantModify, session: Session =Depends(get_session)):
    updated_restaurant=await modify_restaurant(id,data, session)
    return  updated_restaurant


@Restaurant_router.delete("/{id}")
async def delete_restaurant_by_id(id: int, session: Session = Depends(get_session)):
    return await delete_restaurant(id, session)


@Restaurant_router.get("/all/"  , response_model =list[RestaurantResponse])
async def get_all(session:Session = Depends(get_session)):
    all_restaurant=session.query(Restaurants).all()
    return all_restaurant


@Restaurant_router.get("/filter_by_cuisine_or_city/", response_model=list[RestaurantResponse2])
async def get_all(
    cuisine_name: str = Query(None),  # Accept cuisine_name as a query parameter
    city: str = Query(None),  # Accept city as a query parameter
    session: Session = Depends(get_session)
):

    # Start with a base query

    query = session.query(
        Restaurants.id,
        Restaurants.user_id,
        Restaurants.cuisine_id,
        Restaurants.address_id,
        Restaurants.restaurant_name,
        Restaurants.tel_number,
        Restaurants.description,
        Restaurants.pickup_time,

        #Cuisines.id.label("cuisine_id"),
        Cuisines.cuisine_name,  # Add cuisine_name from Cuisines table
        Addresses.id.label("address_id"),
        Addresses.street,  # Add street_name from Addresses table
        Addresses.city,  # Add city from Addresses table
        Addresses.postal_code,  # Add postal_code from Addresses table
        Addresses.flat_number,  # Include flat_number in the query
        Addresses.door_number,  # Include door_number in the query
        Addresses.google_maps_link
    ).join(
        Cuisines, Restaurants.cuisine_id == Cuisines.id
    ).join(
        Addresses, Restaurants.address_id == Addresses.id
    )


    # Apply filters based on the provided parameters

    if cuisine_name and city:
        query = query.filter(
            Cuisines.cuisine_name.ilike(f"%{cuisine_name}%"),
            Addresses.city.ilike(f"%{city}%")
        )

    elif cuisine_name:
        query = query.filter(Cuisines.cuisine_name.ilike(f"%{cuisine_name}%"))
    elif city:
        query = query.filter(Addresses.city.ilike(f"%{city}%"))

    # Execute the query
    all_restaurant = query.all()

    # Construct response
    response_data = [
        RestaurantResponse2(
            id=restaurant.id,
            user_id=restaurant.user_id,
            cuisine=CuisineResponse(
                id=restaurant.cuisine_id,
                cuisine_name=restaurant.cuisine_name
            ),
            address=AdressResponse(
                id=restaurant.address_id,
                street=restaurant.street,
                city=restaurant.city,
                postal_code=restaurant.postal_code,
                flat_number=restaurant.flat_number,
                door_number=restaurant.door_number,
                google_maps_link=restaurant.google_maps_link

            ),

            restaurant_name=restaurant.restaurant_name,
            tel_number=restaurant.tel_number,
            description=restaurant.description,
            pickup_time=restaurant.pickup_time
        )

        for restaurant in all_restaurant
    ]

    return response_data



@Restaurant_router.post("/upload&restaurant/image/" )
async def upload_restaurant_image(image: UploadFile =File(...)):
    upload_dir ="uploads/restaurants"
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
    image_url=f"/uploads/restaurants/{filename}"
    return {"image_url": image_url}

   


@Restaurant_router.patch("/{id}/image", status_code=status.HTTP_200_OK)
async def update_restaurant_image(
    id: int,
    image_update: RestaurantImageUpdate, # Use the new Pydantic schema
    session: Session = Depends(get_session)
):
    """
    Updates only the image_url for a specific restaurant.
    """
    restaurant = session.query(Restaurants).filter(Restaurants.id == id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    # Apply the update
    restaurant.image_url = image_update.image_url
    session.add(restaurant) # Or session.merge(restaurant) depending on your SQLAlchemy setup
    session.commit()
    session.refresh(restaurant) # Refresh to get the latest state from DB
    # Return a success message or the updated image URL
    return {"message": "Restaurant image updated successfully", "image_url": restaurant.image_url}



