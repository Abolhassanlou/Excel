from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import jwt
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from schemas import UserLogin , UserCreate ,UserResponse
from models import User
from database import Base , engine , create_engine , get_db
from datetime import datetime, timedelta
from fastapi import Header 

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT secret
JWT_SECRET = 'myjwtsecret'

SECRET_KEY = "mysecret"  # Change this in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_verification_token(data: dict):
    expiration = datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    to_encode = {"exp": expiration.timestamp(), **data}  # Convert to timestamp
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


# Function to get the current authenticated user
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

# Function to authenticate user
async def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return False
    return user


def verify_token(authorization: str = Header(...)) -> dict:
    try:
        # Extract the token from Authorization header (Bearer <token>)
        token = authorization.split(" ")[1]  # "Bearer <token>"
        
        # Decode and verify the JWT token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        
        # Return the decoded payload (user info)
        return payload
    
    except IndexError:
        raise HTTPException(
            status_code=400,
            detail="Token format is incorrect. Use Bearer <token>"
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )