from fastapi import HTTPException
from app.models.user import Categories
import logging
from app.config.settings import get_settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = get_settings()


async def create_category(data, session):
   category=Categories()
   category.name=data.name
   
   session.add(category)
   session.commit()
   session.refresh(category)
   return category
    
async def modify_category (pk , data , session):
    category=session.query(Categories).filter(Categories.id==pk).first ()

    if not category :
        raise HTTPException(status_code=401 , detail= "Category not find")

    category.name=data.name
    session.commit()
    session.refresh(category)

    return category

async def fetch_category_detail(pk , session):
    category=session.query(Categories).filter(Categories.id==pk).first()
    if category:
        return category
    raise HTTPException(status_code=404 , detail="Category not found")

async def delete_category(id: int, session):
    db_category = session.query(Categories).filter(Categories.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        session.delete(db_category)
        session.commit()
        logger.info(f"Deleted Category with id {id}")
        return {"message": "Category deleted successfully"}
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting category with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")