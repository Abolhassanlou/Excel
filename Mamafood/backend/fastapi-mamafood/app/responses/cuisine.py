from app.responses.base import BaseResponse

class CuisineResponse(BaseResponse):
    id : int
    cuisine_name: str
    