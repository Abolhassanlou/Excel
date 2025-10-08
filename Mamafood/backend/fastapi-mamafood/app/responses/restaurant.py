from app.responses.base import BaseResponse
from datetime import datetime
from app.responses.cuisine import CuisineResponse
from app.responses.address import AdressResponse
from typing import Optional

class RestaurantResponse(BaseResponse): 
    id : int
    user_id :int
    cuisine_id : int
    address_id : int
    restaurant_name : str
    tel_number :str
    description : str
    pickup_time: str
    image_url: Optional[str] = None

class RestaurantResponse2(BaseResponse):
    id: int
    user_id: int
    cuisine: CuisineResponse
    address: AdressResponse
    restaurant_name: str
    tel_number: str
    description: str
    pickup_time: str
    image_url: Optional[str] = None
    
class RestaurantImageUpdate(BaseResponse):
    
    image_url: Optional[str] = None