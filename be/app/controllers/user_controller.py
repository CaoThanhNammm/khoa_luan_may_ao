from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.schemas.user import UserResponse, AccountStats
from app.services import user_service
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.get("/stats", response_model=AccountStats)
def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get account statistics for the current user"""
    stats = user_service.get_account_stats(db, current_user.id)
    return stats