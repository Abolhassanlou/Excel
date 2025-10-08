from fastapi import APIRouter , Depends , status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_session
from app.schemas.Category import RegisterCategory ,ModifyCategory
from app.responses.category import CategoryResponse
from app.services.category import create_category , modify_category , fetch_category_detail , delete_category
from app.models.user import Categories



Category_router=APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description" : "Not found "}}

)

@Category_router.post("" , status_code=status.HTTP_201_CREATED  , response_model=CategoryResponse )
async def register_category (data: RegisterCategory, session: Session =Depends(get_session)):
    return await create_category(data, session)


@Category_router.get("/all/"  , response_model =list[CategoryResponse])
async def get_all(session:Session = Depends(get_session)):
    all_category=session.query(Categories).all()
    return all_category

@Category_router.get ("/pk" , response_model=CategoryResponse)
async def get_by_id(pk :int, session:Session = Depends(get_session)):
    return await fetch_category_detail(pk, session)

@Category_router.put("/{pk}" , status_code=status.HTTP_200_OK , response_model=CategoryResponse)
async def update_category (pk:int , data:ModifyCategory , session:Session =Depends(get_session)):
    updated_category=modify_category(pk, data, session)
    return await updated_category  # Return the updated cuisine as a response

@Category_router.delete("/{id}")
async def delete_category_by_id(id: int, session: Session = Depends(get_session)):
    return await delete_category(id, session)
    

        