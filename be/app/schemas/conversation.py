from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    type: str  # USER or BOT

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    conversation_id: str
    created_at: datetime
    timestamp: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
    
    def __init__(self, **data):
        # Map created_at to timestamp for frontend compatibility
        if 'created_at' in data and 'timestamp' not in data:
            data['timestamp'] = data['created_at']
        super().__init__(**data)

class ConversationBase(BaseModel):
    title: str

class ConversationCreate(BaseModel):
    message: str

class ConversationWithDocumentCreate(BaseModel):
    message: str
    document_id: str

class EmptyConversationWithDocumentCreate(BaseModel):
    document_id: str
    filename: str
    title: Optional[str] = None
    file_size: Optional[int] = None
    status: Optional[str] = None
    s3_key: Optional[str] = None
    s3_url: Optional[str] = None

class DocumentInfo(BaseModel):
    document_id: Optional[str] = None
    filename: str
    file_size: Optional[int] = None
    sentences_count: Optional[int] = None
    upload_date: str
    status: Optional[str] = None
    
    class Config:
        # Convert snake_case to camelCase for frontend
        alias_generator = lambda field_name: ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_')))
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class ConversationResponse(ConversationBase):
    id: str
    user_id: int
    created_at: datetime
    messages: List[MessageResponse] = []
    has_document: Optional[bool] = False
    document_info: Optional[DocumentInfo] = None
    
    class Config:
        from_attributes = True
        # Convert snake_case to camelCase for frontend
        alias_generator = lambda field_name: ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_')))
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class MessageRequest(BaseModel):
    message: str
    document_id: Optional[str] = None

class StudentHandbookConversationCreate(BaseModel):
    """Schema for creating empty conversation for student handbook"""
    pass

class StudentHandbookMessageRequest(BaseModel):
    """Schema for sending message to student handbook (creates conversation if needed)"""
    message: str