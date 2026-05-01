from pydantic import BaseModel,Field
from datetime import datetime
from typing import Literal, Optional, List

class CreateChatSchema(BaseModel):
    message: str

class AddMessageSchema(BaseModel):
    message: str
    chat_id: str 

class FlashcardRequest(BaseModel):
    user_id: str
    content: str        # extracted text from slides/pdf

class SummaryRequest(BaseModel):
    user_id: str
    content: str

class QuestionRequest(BaseModel):
    question: str

