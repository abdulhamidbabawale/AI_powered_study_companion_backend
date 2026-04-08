from pydantic import BaseModel, ValidationError
from app.db.connection import db
from app.db.models import UserModel

collection = db["users"]  

async def create_user(user: UserModel):
    result = await collection.insert_one(user.model_dump(by_alias=True))
    # result = await collection.insert_one(user)
    return str(result.inserted_id)

async def get_user_by_email(email: str):
    return await collection.find_one({"email": email})