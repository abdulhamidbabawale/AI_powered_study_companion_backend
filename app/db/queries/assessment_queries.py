from app.db.connection import db
from app.db.models import AssessmentModel
from datetime import datetime
from fastapi import HTTPException

collection = db["assessments"]

async def create_assessment(assessment: AssessmentModel):
    result = await collection.insert_one(assessment.model_dump(by_alias=True))
    return str(result.inserted_id)

async def get_assessment_by_id(assessment_id: str):
    assessment = await collection.find_one({"_id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

async def get_user_assessments(user_id: str, page: int = 1, limit: int = 10):
    limit = min(limit, 100)
    skip = (page - 1) * limit

    assessments = await collection.find(
        {"user_id": user_id}
    ).sort("due_date", 1).skip(skip).limit(limit).to_list(length=limit)

    total = await collection.count_documents({"user_id": user_id})

    return {
        "data": assessments,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": -(-total // limit)
        }
    }

async def update_assessment(assessment_id: str, updates: dict):
    await collection.update_one(
        {"_id": assessment_id},
        {"$set": {**updates, "updated_at": datetime.now()}}
    )

async def delete_assessment(assessment_id: str):
    result = await collection.delete_one({"_id": assessment_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Assessment not found")