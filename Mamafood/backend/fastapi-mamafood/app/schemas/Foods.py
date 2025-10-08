from pydantic import BaseModel
from typing import List
from decimal import Decimal

class FoodRegister(BaseModel):
    name: str  # Name of the food item
    description: str  # Description of the food item
    price: Decimal  # Price of the food item (Decimal type for proper precision)
    initial_stock: int  # Initial stock of the food item
    preparation_time: str  # Preparation time (e.g., "15:30" or "00:15" for 15 minutes)
    image_url: str  # URL of the food item's image
    categories: List[int]  # List of category IDs this food belongs to
    restaurant_id: int  # ID of the restaurant the food belongs to

class FoodModify(BaseModel):
    name: str  # Name of the food item
    description: str  # Description of the food item
    price: Decimal  # Price of the food item (Decimal type for proper precision)
    initial_stock: int  # Initial stock of the food item
    preparation_time: str  # Preparation time (e.g., "15:30" or "00:15" for 15 minutes)
    image_url: str  # URL of the food item's image
    categories: List[int]  # List of category IDs this food belongs to
    restaurant_id: int  # ID of the restaurant the food belongs to
    
