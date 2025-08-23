from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.schemas.document import DocumentResponse, ContactMessageCreate, ContactMessageResponse
from app.services import document_service
from app.utils.security import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(tags=["Documents"])

@router.post("/api/upload-file", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a file (PDF)"""
    result = await document_service.process_file_upload(file, current_user.id, db)
    return result

@router.get("/api/documents", response_model=List[DocumentResponse])
def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents for the current user"""
    documents = document_service.get_user_documents(db, current_user.id)
    return documents

@router.post("/api/contact", response_model=ContactMessageResponse, status_code=status.HTTP_201_CREATED)
def create_contact_message(
    contact: ContactMessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new contact message"""
    contact_message = document_service.create_contact_message(db, contact)
    return contact_message