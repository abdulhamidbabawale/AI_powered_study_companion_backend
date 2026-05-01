from fastapi import APIRouter, Depends, HTTPException
from app.services.user_services import register_user, login_user
from app.schemas.user_schemas import CreateUserSchema, LoginSchema


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
async def register(user:CreateUserSchema):
    new_user = await register_user(user)
    return {
        "message":"user created successfully",
        "user_id":new_user
    }
    
@router.post("/login")
async def login(credentials: LoginSchema):
    res = await login_user(credentials)
    return {
        "message": "Login successful",
        "access_token": res["access_token"],
        "token_type": "bearer",
        "user":res["user"]
    }