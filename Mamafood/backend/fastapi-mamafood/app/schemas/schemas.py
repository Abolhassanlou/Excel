from pydantic import BaseModel, EmailStr, ConfigDict , ValidationError ,field_validator
from typing import List, Optional 
from datetime import datetime
from typing import Generic , TypeVar
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"])

class RegisterUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    
class VerifyUserRequest(BaseModel):
    token: str
    email: EmailStr
    
class EmailRequest(BaseModel):
    email: EmailStr
    
class ResetRequest(BaseModel):
    token: str
    email: EmailStr
    password: str

class Users(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    registration_date: datetime=None
    first_name: str
    last_name: str
    email: EmailStr
    image_url: Optional[str] = None
    role: int

class UserRead(BaseModel): 
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    image_url: Optional[str] = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    image_url: Optional[str] = None

class Address(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    street: str
    flat_number: Optional[str] = None
    door_number: Optional[str] = None
    city: str
    postal_code: str
    google_maps_link: Optional[str] = None  # Optional for storing a Google Maps link


class AddressCreate(BaseModel):
    street: str
    flat_number: Optional[str] = None
    door_number: Optional[str] = None
    city: str
    postal_code: str
    google_maps_link: Optional[str] = None


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    flat_number: Optional[str] = None
    door_number: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    google_maps_link: Optional[str] = None

# CusineDetails Schema

class Cuisine(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cuisine_name: str

class CuisineCreate(BaseModel):
    cuisine_name: str

class CuisineUpdate(BaseModel):
    cuisine_name: Optional[str] = None

class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cat_name: str

class CategoryCreate(BaseModel):
    cat_name: str


class CategoryUpdate(BaseModel):
    cat_name: Optional[str] = None

# Restaurant Schema
class Restaurant(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    user_id: int
    restaurant_name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    address_id: int
    cuisine_id: int
    

class RestaurantCreate(BaseModel):
    user_id: int
    restaurant_name: str
    cuisine_id: int  # Only one cuisine type ID for each restaurant
    description: Optional[str] = None
    image_url: Optional[str] = None
    address_id: int

class RestaurantUpdate(BaseModel):
    user_id: Optional[int] = None
    restaurant_name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    address_id: Optional[int] = None
    cuisine_id: Optional[int] = None  # Only one cuisine type ID for each restaurant

class Food(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    food_name: str
    description: Optional[str] = None
    cuisine_id: int
    restaurant_id: int
    price: float
    quantity: int
    initial_stock: int  # Corrected from intitial_stock
    image_url: Optional[str] = None
    preparation_time: Optional[int] = None

class FoodCreate(BaseModel):
    food_name: str
    description: Optional[str] = None
    cuisine_id: int
    restaurant_id: int
    price: float
    initial_stock: int  # Corrected from intitial_stock
    image_url: Optional[str] = None
    preparation_time: Optional[int] = None

class FoodUpdate(BaseModel):
    food_name: Optional[str] = None
    description: Optional[str] = None
    cuisine_id: Optional[int] = None
    restaurant_id: Optional[int] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    initial_stock: Optional[int] = None  # Corrected from intitial_stock
    image_url: Optional[str] = None
    preparation_time: Optional[int] = None



