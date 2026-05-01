from app.db.queries.assessment_queries import (
    create_assessment, get_assessment_by_id,
    get_user_assessments, update_assessment, delete_assessment
)
from app.db.models import AssessmentModel
from app.schemas.assessment_schemas import CreateAssessmentSchema, UpdateAssessmentSchema
from fastapi import HTTPException
from datetime import datetime,timezone


async def add_assessment(user_id: str, data: CreateAssessmentSchema):
    # normalize both to naive datetime for comparison
    due_date = data.due_date.replace(tzinfo=None)
    
    if due_date <= datetime.now():
        raise HTTPException(status_code=400, detail="Due date must be in the future")

    if data.reminder_date:
        reminder_date = data.reminder_date.replace(tzinfo=None)
        if reminder_date >= due_date:
            raise HTTPException(status_code=400, detail="Reminder must be before the due date")

    assessment = AssessmentModel(
        user_id=user_id,
        title=data.title,
        assessment_type=data.assessment_type,
        due_date=due_date,
        description=data.description,
        reminder_date=reminder_date if data.reminder_date else None,
    )

    assessment_id = await create_assessment(assessment)
    return await get_assessment_by_id(assessment_id)


async def fetch_assessments(user_id: str, page: int, limit: int):
    return await get_user_assessments(user_id, page, limit)


async def fetch_assessment(assessment_id: str):
    return await get_assessment_by_id(assessment_id)


async def edit_assessment(assessment_id: str, data: UpdateAssessmentSchema):
    updates = data.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    await update_assessment(assessment_id, updates)
    return await get_assessment_by_id(assessment_id)


async def remove_assessment(assessment_id: str):
    await delete_assessment(assessment_id)
    return {"message": "Assessment deleted successfully"}