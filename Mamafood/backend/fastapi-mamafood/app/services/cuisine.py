from fastapi import HTTPException
from app.models.user import Cuisines
import logging
from app.config.settings import get_settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = get_settings()


async def create_cuisine(data, session):
   cuisine=Cuisines()
   cuisine.cuisine_name=data.cuisine_name
   
   session.add(cuisine)
   session.commit()
   session.refresh(cuisine)
   return cuisine
    
async def modify_cuisine (pk , data , session):
    cuisine=session.query(Cuisines).filter(Cuisines.id==pk).first ()

    if not cuisine :
        raise HTTPException(status_code=401 , detail= "Cuisine not find")

    cuisine.cuisine_name=data.cuisine_name
    session.commit()
    session.refresh(cuisine)

    return cuisine

async def fetch_cuisine_detail(pk , session):
    cuisine=session.query(Cuisines).filter(Cuisines.id==pk).first()
    if cuisine:
        return cuisine
    raise HTTPException(status_code=404 , detail="Cusine not found")

async def delete_cuisine(id: int, session):
    db_cuisine = session.query(Cuisines).filter(Cuisines.id == id).first()
    if not db_cuisine:
        raise HTTPException(status_code=404, detail="Cuisine not found")
    try:
        session.delete(db_cuisine)
        session.commit()
        logger.info(f"Deleted Cuisine with id {id}")
        return {"message": "Cuisine deleted successfully"}
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting cuisine with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")