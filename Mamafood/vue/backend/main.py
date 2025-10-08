from fastapi import FastAPI, Depends, HTTPException, status , Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import jwt
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from schemas import UserLogin , UserCreate , UserResponse
from models import User
from database import Base , engine , create_engine , get_db
from security import get_current_user , authenticate_user , JWT_SECRET ,ALGORITHM ,create_verification_token , verify_token
from repositoryuser import SendEmailVerify
import jwt 
from fastapi import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

# FastAPI app setup
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows only the specified origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Check if username or email already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

       
    # Create the user (active = False by default)
    db_user = User(username=user.username, email=user.email, password=bcrypt.hash(user.password), is_active=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate the verification token
    token = create_verification_token({"username": db_user.username})
    
    # Send the verification email with the token
    background_tasks.add_task(SendEmailVerify.sendVerify, token)  # token = security.create_verification_token({"username": db_user.username})
    
    return db_user

@app.get("/user/verify/{token}")
def verify_user(token: str, db: Session = Depends(get_db)):
    try:
        # Decode the token to get the username
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("username")
        
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        
        # Find the user in the database
        db_user = db.query(User).filter(User.username == username).first()
        
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if the user is already active
        if db_user.is_active:
            raise HTTPException(status_code=400, detail="User is already active")
        
        # Activate the user
        db_user.is_active = True
        db.commit()
        
        return {"message": "User activated successfully"}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    
    except :
        raise HTTPException(status_code=400, detail="Invalid token")

# Function to create a JWT token
@app.post("/login")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create the JWT token with user information
    token = jwt.encode({"id": user.id, "email": user.email}, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(user_info: dict = Depends(verify_token)):
    # The user is authenticated and their information is in 'user_info'
    return {"message": "This is a protected route", "user": user_info}

# Route to get the current logged-in user
@app.get("/users/me", response_model=UserLogin)
async def read_users_me(current_user: UserLogin = Depends(get_current_user)):
    return current_user

