from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, AccountStats
from app.utils.security import get_password_hash, verify_password
from fastapi import HTTPException, status
from typing import Optional

def get_user_by_id(db: Session, user_id: int):
    """Get a user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Get a user by username"""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Get a user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_reset_token(db: Session, token: str):
    """Get a user by password reset token"""
    return db.query(User).filter(User.password_reset_token == token).first()

def create_user(db: Session, user: UserCreate):
    """Create a new user"""
    # Check if username already exists
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )
    
    # Check if email already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already in use"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def update_password(db: Session, user: User, new_password: str):
    """Update a user's password"""
    user.password = get_password_hash(new_password)
    user.clear_password_reset_token()
    db.commit()
    db.refresh(user)
    return user

def get_account_stats(db: Session, user_id: int) -> AccountStats:
    """Get account statistics for a user"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Count conversations
    total_conversations = len(user.conversations)
    
    # Count documents
    total_documents = len(user.documents)
    
    # Count messages
    total_messages = 0
    for conversation in user.conversations:
        total_messages += len(conversation.messages)
    
    return AccountStats(
        total_conversations=total_conversations,
        total_documents=total_documents,
        total_messages=total_messages
    )