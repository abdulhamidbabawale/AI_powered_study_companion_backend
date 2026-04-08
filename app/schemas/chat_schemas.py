from pydantic import BaseModel,Field
from datetime import datetime
from typing import Literal, Optional, List

# class CreateChatSchema(BaseModel):
#     user_id: str
#     title: Optional[str] = None

# class AddMessageSchema(BaseModel):
#     role:Literal["user", "assistant", "system"]
#     content: str

class CreateChatSchema(BaseModel):
    user_id: str
    message: str

class AddMessageSchema(BaseModel):
    user_id: str
    message: str
    chat_id: str 

class FlashcardRequest(BaseModel):
    user_id: str
    content: str        # extracted text from slides/pdf

class SummaryRequest(BaseModel):
    user_id: str
    content: str

class QuestionRequest(BaseModel):
    user_id: str
    content: str
    question: str
    chat_id: Optional[str] = None

# class Message(BaseModel):
#     role: Literal["user", "assistant", "system"]
#     content: str
#     timestamp: datetime = datetime.utcnow()

# class Chat(BaseModel):
#     id: Optional[str] = Field(alias="_id")
#     user_id: str
#     title: Optional[str] = None
#     messages: List[Message] = []
#     created_at: datetime = datetime.utcnow()
#     updated_at: datetime = datetime.utcnow()

#     class Config:
#         populate_by_name = True