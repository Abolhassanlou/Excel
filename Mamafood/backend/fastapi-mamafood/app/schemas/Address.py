
from pydantic import BaseModel, Field, ConfigDict # Import Field and ConfigDict
from typing import Optional # Import Optional


class RegisterAddress(BaseModel):
    street : str
    city : str
    postal_code : str
    flat_number : str
    door_number : str
    google_maps_link: Optional[str] = Field(None, alias="google_maps_link")
    

class ModifyAddress(BaseModel):
    street : str
    city : str
    postal_code : str
    flat_number : str
    door_number : str
    google_maps_link : str
    
    

    