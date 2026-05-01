from fastapi import APIRouter, Depends
from app.services.assessment_services import (
    add_assessment, fetch_assessments,
    fetch_assessment, edit_assessment, remove_assessment
)
from app.schemas.assessment_schemas import CreateAssessmentSchema, UpdateAssessmentSchema
from app.jwt import get_current_user

router = APIRouter(prefix="/assessments", tags=["assessments"])

@router.post("/", status_code=201)
async def create(body: CreateAssessmentSchema, user_id: str = Depends(get_current_user)):
    return await add_assessment(user_id, body)

@router.get("/")
async def get_all(user_id: str = Depends(get_current_user), page: int = 1, limit: int = 10):
    return await fetch_assessments(user_id, page, limit)

@router.get("/{assessment_id}")
async def get_one(assessment_id: str, _: str = Depends(get_current_user)):
    return await fetch_assessment(assessment_id)

@router.patch("/{assessment_id}")
async def update(assessment_id: str, body: UpdateAssessmentSchema, _: str = Depends(get_current_user)):
    return await edit_assessment(assessment_id, body)

@router.patch("/{assessment_id}/complete")
async def complete(assessment_id: str, _: str = Depends(get_current_user)):
    return await edit_assessment(assessment_id, UpdateAssessmentSchema(is_completed=True))

@router.delete("/{assessment_id}")
async def delete(assessment_id: str, _: str = Depends(get_current_user)):
    return await remove_assessment(assessment_id)