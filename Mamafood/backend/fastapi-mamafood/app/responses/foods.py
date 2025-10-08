from app.responses.base import BaseResponse
from typing import List
from datetime import time
from decimal import Decimal
from typing import Optional

class CuisineResponse(BaseResponse):
    id: int
    cuisine_name: str

class RestaurantResponse(BaseResponse):
    id: int
    restaurant_name: str 
    cuisine: CuisineResponse

class CategroyResponse(BaseResponse):
    id:int 
    name: str

class FoodResponse (BaseResponse):
    id :int
    name :str
    description :str
    restaurant_id :int
    price :Decimal
    initial_stock :int
    preparation_time:  time
    image_url :str
    categories : List[CategroyResponse]
    restaurant : RestaurantResponse

class FoodImageUpdate(BaseResponse):
    
    image_url: Optional[str] = None

 