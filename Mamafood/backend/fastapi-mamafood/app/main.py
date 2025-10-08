from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes import user, address , cuisine , restaurant , category , foods
from fastapi.staticfiles import StaticFiles
import os

def create_application():
    application = FastAPI()

    application.include_router(user.user_router)
    application.include_router(user.guest_router)
    application.include_router(user.auth_router)
    application.include_router(address.Address_router)
    application.include_router(cuisine.Cuisine_router)
    application.include_router(restaurant.Restaurant_router)
    application.include_router(category.Category_router)
    application.include_router(foods.Food_router)
    
    application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows only the specified origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    return application


app = create_application()
BASE_DIR = os.path.dirname(__file__)  # یعنی /usr/srv/app
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# ساخت پوشه اگر وجود ندارد
os.makedirs(os.path.join(UPLOAD_DIR, "restaurants"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "foods"), exist_ok=True)

# mount کردن مسیر
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")



@app.get("/")
async def root():
    return {"message": "Hi, I am mamafood. Awesome - Your setrup is done & working."}