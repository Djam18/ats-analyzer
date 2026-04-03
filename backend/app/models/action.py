import uuid
from sqlalchemy import Column, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from app.models.base import Base
 
class ActionLog(Base):
    __tablename__ = "action_log"
    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("application.id", ondelete="CASCADE"), nullable=False)
    user_id        = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    action_type    = Column(String(50), nullable=False)
    old_value      = Column(String(255))
    new_value      = Column(String(255))
    comment        = Column(Text)
    created_at     = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (Index("ix_action_log_application_id", "application_id", "created_at"),)
    application    = relationship("Application", back_populates="action_logs")
    user           = relationship("User",        back_populates="action_logs")
 
class InternalNote(Base):
    __tablename__ = "internal_note"
    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("application.id", ondelete="CASCADE"), nullable=False)
    user_id        = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    content        = Column(Text, nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    application    = relationship("Application", back_populates="internal_notes")
    user           = relationship("User",        back_populates="internal_notes")
