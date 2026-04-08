from pydantic import BaseModel, ValidationError
from app.db.connection import db
from app.db.models import ChatModel,MessageModel
from datetime import datetime
from fastapi import HTTPException

collection = db["chats"] 

async def create_chat(chat:ChatModel):
    new_chat= await collection.insert_one(chat.model_dump(by_alias=True))
    return str(new_chat.inserted_id)

async def append_message(chat_id: str, message: MessageModel):
    await collection.update_one(
        {"_id": chat_id},
        {
            "$push": {"messages": message.model_dump()},
            "$set": {"updated_at": datetime.now()}
        }
    )

async def get_chat_by_id(chat_id: str):
    chat = await collection.find_one({"_id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

async def get_chats(id: str, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit

    chats = await collection.find({"user_id": id}) \
        .skip(skip) \
        .limit(limit) \
        .to_list(length=limit)

    total = await collection.count_documents({"user_id": id})

    return {
        "data": chats,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": -(-total // limit)  # ceiling division
        }
    }