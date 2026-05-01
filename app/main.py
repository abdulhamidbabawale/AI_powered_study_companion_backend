from fastapi import FastAPI
from app.services.user_services import register_user
from app.routers import ai_routes,assessment_routes,users_routes,material_routes 
import uvicorn
from dotenv import load_dotenv
from fastapi.security import HTTPBearer

load_dotenv()  

security = HTTPBearer()
app = FastAPI(
    title="AI Study Companion",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}  # keeps token after page refresh
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_routes.router, prefix='/api/v1')
app.include_router(ai_routes.router, prefix="/api/v1")
app.include_router(material_routes.router, prefix="/api/v1")
app.include_router(assessment_routes.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

