from fastapi import HTTPException , Query
from app.models.user import Restaurants , Addresses , User
import logging
from app.config.settings import get_settings
from app.responses.restaurant import RestaurantResponse
from app.schemas.Restaurant import RestaurantCreateForDB
from app.services.user import create_user_account

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = get_settings()
async def create_restaurant(data: RestaurantCreateForDB, session):
    # This helper accepts data that's ready for the DB, including IDs.
    restaurant = Restaurants(
        user_id=data.user_id,
        cuisine_id=data.cuisine_id,
        address_id=data.address_id,
        restaurant_name=data.restaurant_name,
        tel_number=data.tel_number,
        description=data.description,
        pickup_time=data.pickup_time,
        image_url=data.image_url,
        is_active=False
    )
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant

# Modify an existing restaurant
async def modify_restaurant(pk: int, data , session):
    restaurant = session.query(Restaurants).filter(Restaurants.id == pk).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Update the restaurant details
    restaurant.user_id = data.user_id
    restaurant.cuisine_id = data.cuisine_id
    restaurant.address_id = data.address_id
    restaurant.restaurant_name = data.restaurant_name
    restaurant.tel_number = data.tel_number
    restaurant.description = data.description
    restaurant.pickup_time = data.pickup_time  # Ensure pickup_time is updated as string

    session.commit()
    session.refresh(restaurant)

    return restaurant

# Fetch the details of a specific restaurant
async def fetch_restaurant_detail(pk: int, session):
    restaurant = session.query(Restaurants).filter(Restaurants.id == pk).first()
    if restaurant:
        return restaurant
    raise HTTPException(status_code=404, detail="Restaurant not found")

# Delete a restaurant
async def delete_restaurant(id: int, session):
    db_restaurant = session.query(Restaurants).filter(Restaurants.id == id).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    try:
        session.delete(db_restaurant)
        session.commit()
        logger.info(f"Deleted restaurant with id {id}")
        return {"message": "Restaurant deleted successfully"}
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting restaurant with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
def filter_restaurants(
    db,
    cuisine_id: int = None,
    restaurant_name: str = None,
    street_name: str = None,
    city: str = None,
    postal_code: str = None,
    tel_number: str = None,
):
    # Start the query and join with the Addresses table
    query = db.query(Restaurants).join(Addresses, Restaurants.address_id == Addresses.id)

    # Add filters only if parameters are provided
    if cuisine_id:
        query = query.filter(Restaurants.cuisine_id == cuisine_id)
    if restaurant_name:
        query = query.filter(Restaurants.restaurant_name.ilike(f"%{restaurant_name}%"))
    if street_name:
        query = query.filter(Addresses.street_name.ilike(f"%{street_name}%"))
    if city:
        query = query.filter(Addresses.city.ilike(f"%{city}%"))
    if postal_code:
        query = query.filter(Addresses.postal_code == postal_code)  # Exact match
    if tel_number:
        query = query.filter(Restaurants.tel_number == tel_number)  # Exact match

    return query
