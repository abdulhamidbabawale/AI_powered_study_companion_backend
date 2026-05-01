from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.models import AssessmentType

class CreateAssessmentSchema(BaseModel):
    title: str
    assessment_type: AssessmentType
    due_date: datetime
    description: Optional[str] = None
    reminder_date: Optional[datetime] = None

class UpdateAssessmentSchema(BaseModel):
    title: Optional[str] = None
    assessment_type: Optional[AssessmentType] = None
    due_date: Optional[datetime] = None
    description: Optional[str] = None
    reminder_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    