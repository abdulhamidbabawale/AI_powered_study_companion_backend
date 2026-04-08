from fastapi import FastAPI
from app.services.user_services import register_user
from app.routers import ai_routes
from app.routers import users_routes
import uvicorn
from dotenv import load_dotenv

load_dotenv()  

app = FastAPI()

app.include_router(users_routes.router, prefix='/api/v1')
app.include_router(ai_routes.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/register")
# async def register(user:dict):
#     new_user = await register_user(user)
#     return 'created'
