
from fastapi import APIRouter ,Depends, status , HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config.database import get_session
from app.responses.address import AdressResponse
from app.schemas.Address import RegisterAddress , ModifyAddress
from app.services import address
from app.models.user import Addresses
from typing import List
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

Address_router = APIRouter(
    prefix="/address",
    tags=["Addresses"],
    responses={404: {"description": "Not found"}},
)

@Address_router.post("", status_code=status.HTTP_201_CREATED, response_model=AdressResponse)
async def register_address(data: RegisterAddress,  session: Session = Depends(get_session)):
    return await address.create_address(data, session)

@Address_router.put("/{id}" , response_model=AdressResponse)
async def update_address(id: int, addresses: ModifyAddress, session: Session = Depends(get_session)):
    return await address.modify_adress(id , addresses , session)


@Address_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=AdressResponse)
async def get_address_info(pk, session: Session = Depends(get_session)):
    return await address.fetch_address_detail(pk, session)

@Address_router.get("/all/", response_model=List[AdressResponse])
async def get_all_addresses(session: Session = Depends(get_session)):
    all_addresses = session.query(Addresses).all()
    if not all_addresses:
        raise HTTPException(status_code=404, detail="No addresses found")
    logger.info(f"Fetched {len(all_addresses)} addresses")
    return all_addresses