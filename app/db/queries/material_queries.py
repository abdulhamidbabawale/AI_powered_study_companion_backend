from app.db.connection import db
from app.db.models import MaterialModel
from datetime import datetime
from fastapi import HTTPException

collection = db["materials"]

async def save_material(material: MaterialModel):
    result = await collection.insert_one(material.model_dump(by_alias=True))
    return str(result.inserted_id)

async def get_material_by_id(material_id: str):
    material = await collection.find_one({"_id": material_id})
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

async def get_material_by_chat_id(chat_id: str):
    material = await collection.find_one({"chat_id": chat_id})
    if not material:
        raise HTTPException(status_code=404, detail="No material found for this chat")
    return material

async def get_user_materials(user_id: str, page: int = 1, limit: int = 10):
    limit = min(limit, 100)
    skip = (page - 1) * limit

    materials = await collection.find(
        {"user_id": user_id},
        {"raw_text": 0}
    ).skip(skip).limit(limit).to_list(length=limit)

    total = await collection.count_documents({"user_id": user_id})

    return {
        "data": materials,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": -(-total // limit)
        }
    }

async def update_material(material_id: str, updates: dict):
    await collection.update_one(
        {"_id": material_id},
        {"$set": {**updates, "updated_at": datetime.now()}}
    )