import enum
import uuid

from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.models.base import Base


class UserRole(str, enum.Enum):
    recruiter = "recruiter"
    admin = "admin"


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.recruiter)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    action_logs = relationship("ActionLog", back_populates="user")
    internal_notes = relationship("InternalNote", back_populates="user")
    email_logs = relationship("EmailLog", back_populates="user")
    job_postings = relationship("JobPosting", back_populates="created_by")
