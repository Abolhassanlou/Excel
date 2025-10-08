from fastapi import APIRouter , Depends , status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_session
from app.schemas.Cuisine import RegisterCuisine ,ModifyCuisine
from app.responses.cuisine import CuisineResponse 
from app.services.cuisine import create_cuisine , modify_cuisine , fetch_cuisine_detail , delete_cuisine
from app.models.user import Cuisines



Cuisine_router=APIRouter(
    prefix="/cuisine",
    tags=["Cuisines"],
    responses={404: {"description" : "Not found "}}

)

@Cuisine_router.post("" , status_code=status.HTTP_201_CREATED  , response_model=CuisineResponse )
async def register_cuisine (data: RegisterCuisine, session: Session =Depends(get_session)):
    return await create_cuisine(data, session)


@Cuisine_router.get("/all/"  , response_model =list[CuisineResponse])
async def get_all(session:Session = Depends(get_session)):
    all_cuisine=session.query(Cuisines).all()
    return all_cuisine

@Cuisine_router.get ("/pk" , response_model=CuisineResponse)
async def get_by_id(pk :int, session:Session = Depends(get_session)):
    return await fetch_cuisine_detail(pk, session)

@Cuisine_router.put("/{pk}" , status_code=status.HTTP_200_OK , response_model=CuisineResponse)
async def update_cuisine (pk:int , data:ModifyCuisine , session:Session =Depends(get_session)):
    updated_cuisine=modify_cuisine(pk, data, session)
    return await updated_cuisine  # Return the updated cuisine as a response

@Cuisine_router.delete("/{id}")
async def delete_cuisine_by_id(id: int, session: Session = Depends(get_session)):
    return await delete_cuisine(id, session)
    

        