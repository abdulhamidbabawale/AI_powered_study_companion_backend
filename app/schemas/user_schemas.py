from pydantic import BaseModel, ValidationError, EmailStr, Field,ConfigDict
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    # TEACHER = "teacher"
    ADMIN = "admin"
class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_no: Optional[str] = None        
    password: str    
    role: UserRole = UserRole.USER

class LoginSchema(BaseModel):
    email: EmailStr
    password: str                       
