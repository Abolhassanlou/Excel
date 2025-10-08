from fastapi import HTTPException
from app.models.user import Foods , t_foodcats
import logging
from app.config.settings import get_settings
from sqlalchemy.future import select 
from sqlalchemy.ext.asyncio import AsyncSession

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = get_settings()


 


async def fetch_food_detail(pk , session):
    food=session.query(Foods).filter(Foods.id==pk).first()
    if food:
        return food
    raise HTTPException(status_code=404 , detail="Cusine not found")

async def delete_food(id: int, session):
    db_food = session.query(Foods).filter(Foods.id == id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Cuisine not found")
    try:
        session.delete(db_food)
        session.commit()
        logger.info(f"Deleted Food with id {id}")
        return {"message": "Food deleted successfully"}
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting Food with ID {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")