from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database.base import Base
import uuid
from datetime import datetime, timedelta

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    password_reset_token = Column(String(255), nullable=True)
    password_reset_token_expiry = Column(DateTime, nullable=True)
    
    def set_password_reset_token(self):
        """Generate a password reset token and set expiry to 24 hours from now"""
        self.password_reset_token = str(uuid.uuid4())
        self.password_reset_token_expiry = datetime.now() + timedelta(hours=24)
        
    def clear_password_reset_token(self):
        """Clear the password reset token and expiry"""
        self.password_reset_token = None
        self.password_reset_token_expiry = None
        
    def is_token_valid(self):
        """Check if the password reset token is valid (not expired)"""
        if not self.password_reset_token or not self.password_reset_token_expiry:
            return False
        return datetime.now() < self.password_reset_token_expiry