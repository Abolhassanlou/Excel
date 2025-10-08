

from datetime import datetime, timedelta
import logging
from fastapi import HTTPException 
from sqlalchemy.orm import Session
from app.models.user import Addresses
from app.config.settings import get_settings
from app.schemas.Address import ModifyAddress
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = get_settings()

async def create_address(data, session):
      
    address = Addresses(
    street = data.street,
    city = data.city,
    postal_code = data.postal_code,
    flat_number = data.flat_number,
    door_number = data.door_number,
    google_maps_link=data.google_maps_link
    )

    session.add(address)
    session.commit()
    session.refresh(address)
      
    return address
    
 
    
"""async def modify_address(pk, data, session):
    address=session.query(Addresses).filter(Addresses.id==pk).first()
    if not address:
        raise HTTPException(status_code=404 , detail="Address not found")
    
    address.street = data.street
    address.city = data.city
    address.postal_code = data.postal_code
    address.flat_number = data.flat_number
    address.door_number = data.door_number
    address.google_maps_link=data.google_maps_link
    
    session.commit()
    session.refresh(address)
    
    return address"""

async def modify_adress(id: int, address: ModifyAddress, session: Session):
    db_address = session.query(Addresses).filter(Addresses.id == id).first()

    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")

    for key, value in address.dict(exclude_unset=True).items():
        setattr(db_address, key, value)

    try:
        session.commit()
        session.refresh(db_address)
        logger.info(f"Updated address with ID {id}")
        return db_address
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating address: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    
async def fetch_address_detail(pk, session):
    address = session.query(Addresses).filter(Addresses.id == pk).first()
    if address:
        return address
    raise HTTPException(status_code=404, detail="Address not found.") # 404 more precise than 400