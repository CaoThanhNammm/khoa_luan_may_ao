from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    email: str

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

class AccountStats(BaseModel):
    total_conversations: int
    total_documents: int
    total_messages: int