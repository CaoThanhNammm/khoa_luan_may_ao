from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.schemas.user import UserCreate, Token, PasswordReset, PasswordResetConfirm
from app.services import user_service
from app.utils.security import create_access_token, get_password_hash
from app.utils.email import send_password_reset_email
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Handle preflight requests for auth endpoints
@router.options("/login")
@router.options("/register")
@router.options("/forgot-password")
@router.options("/reset-password")
def auth_options():
    return {"message": "OK"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db), response: Response = None):
    """Register a new user"""
    try:
        db_user = user_service.create_user(db, user)
        
        # Set CORS headers explicitly
        if response:
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return {
            "message": "User registered successfully",
            "user_id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/forgot-password")
def forgot_password(request: PasswordReset, db: Session = Depends(get_db)):
    """Request password reset"""
    # Find user by email
    user = user_service.get_user_by_email(db, request.email)
    
    # Always return success to prevent email enumeration
    if not user:
        return {"message": "If your email exists in our system, we've sent a password reset link."}
    
    # Generate reset token
    user.set_password_reset_token()
    db.commit()
    
    # Send email
    send_password_reset_email(user.email, user.password_reset_token)
    
    # For development, include the reset token in the response
    return {
        "message": "If your email exists in our system, we've sent a password reset link.",
        "resetLink": f"/reset-password?token={user.password_reset_token}",
        "resetToken": user.password_reset_token
    }

@router.post("/reset-password")
def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password with token"""
    # Find user by token
    user = user_service.get_user_by_reset_token(db, request.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    # Check if token is valid (not expired)
    if not user.is_token_valid():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired"
        )
    
    # Update password
    user_service.update_password(db, user, request.new_password)
    
    return {"message": "Password has been reset successfully"}