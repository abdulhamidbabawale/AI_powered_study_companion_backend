from pydantic import BaseModel, ValidationError, EmailStr, Field,ConfigDict
from uuid import UUID, uuid4
from typing import Literal, Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")

    first_name: str
    last_name: str
    email: EmailStr
    phone_no: Optional[str] = None        
    hashed_password: str                  
    role: UserRole = UserRole.USER
    is_active: bool = True
    is_verified: bool = False             # email verification gate
    onboarding_complete: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None # None until first login

class MessageModel(BaseModel):
    role: Literal["user", "model", "system"]
    content: str
    timestamp: datetime = datetime.utcnow()

class ChatModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")

    user_id: str
    title: Optional[str] = None
    messages: List[MessageModel] = []
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
