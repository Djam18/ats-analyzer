import enum
import uuid

from sqlalchemy import Boolean, Column, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.models.base import Base


class EmailStatus(str, enum.Enum):
    success = "success"
    failed = "failed"


class EmailTemplate(Base):
    __tablename__ = "email_template"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    subject = Column(String(255), nullable=False)
    body_html = Column(Text)
    body_text = Column(Text)
    is_default = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    email_logs = relationship("EmailLog", back_populates="email_template")


class EmailLog(Base):
    __tablename__ = "email_log"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(
        UUID(as_uuid=True), ForeignKey("application.id", ondelete="CASCADE"), nullable=False
    )
    email_template_id = Column(
        UUID(as_uuid=True), ForeignKey("email_template.id", ondelete="SET NULL")
    )
    subject_sent = Column(String(255), nullable=False)
    recipient = Column(String(255), nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(Enum(EmailStatus), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    application = relationship("Application", back_populates="email_logs")
    email_template = relationship("EmailTemplate", back_populates="email_logs")
    user = relationship("User", back_populates="email_logs")
