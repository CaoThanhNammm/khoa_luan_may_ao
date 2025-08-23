from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.base import get_db
from app.models.user import User
from app.schemas.conversation import ConversationResponse, ConversationCreate, ConversationWithDocumentCreate, \
    EmptyConversationWithDocumentCreate, MessageResponse, MessageRequest, StudentHandbookConversationCreate, \
    StudentHandbookMessageRequest
from app.services import chat_service
from app.services.chat_service import convert_message_to_response
from app.utils.security import get_current_user
from app.models.document import UserDocument
router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user"""
    conversations = chat_service.get_user_conversations(db, current_user.id)
    return conversations

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific conversation"""
    conversation = chat_service.get_conversation(db, conversation_id)
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return conversation

@router.post("/conversations", response_model=ConversationResponse)
def start_conversation(
    request: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new conversation (default: student handbook)"""
    conversation = chat_service.start_new_conversation(db, current_user.id, request.message, is_student_handbook=True)
    return conversation

@router.post("/conversations/with-document", response_model=ConversationResponse)
def start_conversation_with_document(
    request: ConversationWithDocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new conversation with a document context"""
    conversation = chat_service.start_new_conversation_with_document(
        db, current_user.id, request.message, request.document_id
    )
    return conversation

@router.post("/conversations/empty-with-document", response_model=ConversationResponse)
def create_empty_conversation_with_document(
    request: EmptyConversationWithDocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an empty conversation with document info"""
    conversation = chat_service.create_empty_conversation_with_document(
        db, 
        current_user.id, 
        request.document_id, 
        request.filename,
        request.title,
        request.file_size,
        request.status,
        request.s3_key,
        request.s3_url
    )
    return conversation

@router.post("/conversations/{conversation_id}/messages_stsv", response_model=MessageResponse)
def send_message_stsv(
    conversation_id: str,
    request: MessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in a conversation"""
    message = chat_service.send_message_stsv(db, conversation_id, request.message, current_user.id)
    # Convert SQLAlchemy model to Pydantic model
    return convert_message_to_response(message)

@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
def send_message(
    conversation_id: str,
    request: MessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in a conversation - document_id will be automatically retrieved from database"""
    message = chat_service.send_message(db, conversation_id, request.document_id or "", request.message, current_user.id)
    # Convert SQLAlchemy model to Pydantic model
    return convert_message_to_response(message)

@router.post("/student-handbook/conversations", response_model=ConversationResponse)
def create_student_handbook_conversation(
    request: StudentHandbookConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create an empty conversation for student handbook"""
    conversation = chat_service.create_empty_student_handbook_conversation(db, current_user.id)
    return conversation

@router.post("/student-handbook/messages", response_model=MessageResponse)
def send_message_to_student_handbook(
    request: StudentHandbookMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to student handbook. Creates new conversation automatically."""
    message = chat_service.send_message_to_student_handbook(
        db, request.message, current_user.id
    )
    # Convert SQLAlchemy model to Pydantic model
    return convert_message_to_response(message)

@router.post("/student-handbook/conversations/{conversation_id}/messages", response_model=MessageResponse)
def send_message_to_existing_student_handbook_conversation(
    conversation_id: str,
    request: StudentHandbookMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to an existing student handbook conversation"""
    message = chat_service.send_message_to_student_handbook(
        db, request.message, current_user.id, conversation_id
    )
    # Convert SQLAlchemy model to Pydantic model
    return convert_message_to_response(message)

@router.get("/cache-info")
def get_cache_info(
    current_user: User = Depends(get_current_user)
):
    """Get cache information for debugging"""
    return chat_service.get_cache_info()

@router.get("/debug/conversation/{conversation_id}/user-document")
def debug_user_document(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Debug endpoint to check user_document for a conversation"""
    user_document = db.query(UserDocument).filter(
        UserDocument.conversation_id == conversation_id
    ).first()
    
    if user_document:
        return {
            "found": True,
            "user_id": user_document.user_id,
            "conversation_id": user_document.conversation_id,
            "document_id": user_document.document_id,
            "filename": user_document.filename,
            "created_at": user_document.created_at.isoformat() if user_document.created_at else None
        }
    else:
        return {"found": False}

@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    deleted = chat_service.delete_conversation(db, conversation_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or access denied"
        )
    return {"message": "Conversation deleted successfully"}