from app.responses.base import BaseResponse
from typing import Optional
class AdressResponse(BaseResponse):
    id : int
    street : str
    city : str
    postal_code : str
    flat_number : str
    door_number :str
    google_maps_link : Optional[str] = None
    