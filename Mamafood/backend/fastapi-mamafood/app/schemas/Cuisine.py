from pydantic import BaseModel

class RegisterCuisine (BaseModel):
    cuisine_name: str

class ModifyCuisine (BaseModel): 
    cuisine_name: str  