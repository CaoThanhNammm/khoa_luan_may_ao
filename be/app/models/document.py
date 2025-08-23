from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class UserDocument(Base):
    __tablename__ = "user_documents"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=True)
    document_id = Column(String(255), nullable=True)  # External document ID (e.g., UUID for S3)
    filename = Column(String(255), nullable=False)
    file_size = Column(BigInteger, nullable=True)
    status = Column(String(50), nullable=True, default="processing")  # processing, done, error
    s3_key = Column(String(255), nullable=True)
    s3_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="documents")
    conversation = relationship("Conversation", back_populates="documents")

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())