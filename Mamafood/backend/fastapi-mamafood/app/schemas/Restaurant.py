from pydantic import BaseModel 
from app.schemas.user import RegisterUserRequest
from app.schemas.Address  import RegisterAddress
from typing import Optional

class RestuarantRegister(BaseModel):
    cuisine_id : int
    restaurant_name : str
    tel_number :str
    description : str
    pickup_time: str
    image_url: Optional[str] = None

class RestaurantRegistrationRequest(BaseModel):
    user: RegisterUserRequest            # Nested User details
    address: RegisterAddress       # Nested Address details
    restaurant: RestuarantRegister # Nested Restaurant details

class RestaurantCreateForDB(BaseModel):
    user_id: int
    cuisine_id: int
    address_id: int
    restaurant_name: str
    tel_number: str
    description: str
    pickup_time: str
    image_url: Optional[str] = None

class RestaurantModify(BaseModel):
    user_id :int
    cuisine_id : int
    address_id : int
    restaurant_name : str
    tel_number :str
    description : str
    pickup_time: str

