from fastapi import APIRouter , Depends , status , Query , HTTPException 
from fastapi.responses import JSONResponse 
from sqlalchemy.orm import Session
from app.config.database import get_session
from app.schemas.Restaurant import RestaurantModify , RestuarantRegister
from app.responses.restaurant import RestaurantResponse , RestaurantResponse2
from app.responses.cuisine import CuisineResponse
from app.responses.address import AdressResponse
from app.services.restaurant import create_restaurant , modify_restaurant , fetch_restaurant_detail , delete_restaurant , filter_restaurants
from app.models.user import Restaurants , Cuisines ,Addresses


Restaurant_router=APIRouter(
    prefix="/restaurant" , 
    tags=["restaurants"],
    responses={404: {"description" : "Not found "}}
)

@Restaurant_router.post("" , status_code=status.HTTP_200_OK , response_model=RestaurantResponse)
async def register_restaurant(data:RestuarantRegister, session: Session=Depends(get_session)):
    return await create_restaurant(data, session)

@Restaurant_router.get("/{id}" , response_model=RestaurantResponse)
async def get_by_id(id:int , session:Session=Depends(get_session)):
    return await fetch_restaurant_detail (id , session)


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

""""@Restaurant_router.get("/all_cname/", response_model=list[RestaurantResponse])
async def get_all(
    cuisine_name: str = Query(None),  # Accept cuisine_name as a query parameter
    session: Session = Depends(get_session)
):
    # If cuisine_name is provided, filter restaurants by it
    if cuisine_name:
        all_restaurant = session.query(Restaurants).join(Cuisines, Restaurants.cuisine_id == Cuisines.id).filter(
            Cuisines.cuisine_name.ilike(f"%{cuisine_name}%")
        ).all()
    else:
        # Otherwise, return all restaurants
        all_restaurant = session.query(Restaurants).all()

    return all_restaurant"""

"""@Restaurant_router.get("/allc/", response_model=list[RestaurantResponse])
async def get_all(
    cuisine_id: int = Query(None),  # Accept cuisine_id as a query parameter
    session: Session = Depends(get_session)
):
    # If cuisine_id is provided, filter restaurants by it
    if cuisine_id:
        all_restaurant = session.query(Restaurants).filter(Restaurants.cuisine_id == cuisine_id).all()
    else:
        # Otherwise, return all restaurants
        all_restaurant = session.query(Restaurants).all()

    return all_restaurant"""

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


    