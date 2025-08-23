from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    document_id: str
    filename: str

class DocumentCreate(DocumentBase):
    conversation_id: Optional[str] = None
    file_size: Optional[int] = None
    status: Optional[str] = "processing"
    s3_key: Optional[str] = None
    s3_url: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    conversation_id: Optional[str] = None
    file_size: Optional[int] = None
    status: Optional[str] = None
    s3_key: Optional[str] = None
    s3_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(..., min_length=3, max_length=255)
    message: str = Field(..., min_length=10)

class ContactMessageResponse(ContactMessageCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionRequest(BaseModel):
    question: str
    document_id: Optional[str] = None