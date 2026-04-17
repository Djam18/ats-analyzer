import enum
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.models.base import Base
from app.models.types import INETType as INET
from app.models.types import JSONBType as JSONB


class ApplicationStage(str, enum.Enum):
    received = "received"
    shortlisted = "shortlisted"
    hr_interview = "hr_interview"
    tech_interview = "tech_interview"
    offer = "offer"
    hired = "hired"


class EducationLevel(str, enum.Enum):
    not_specified = "not_specified"
    bac2 = "bac2"
    bac3 = "bac3"
    bac5 = "bac5"
    phd = "phd"


class ParsingStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class Application(Base):
    __tablename__ = "application"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_posting_id = Column(
        UUID(as_uuid=True), ForeignKey("job_posting.id", ondelete="CASCADE"), nullable=False
    )
    candidate_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    stage = Column(Enum(ApplicationStage), nullable=False, default=ApplicationStage.received)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ip_address = Column(INET)
    user_agent = Column(Text)
    gdpr_consent = Column(Boolean, nullable=False)
    gdpr_consent_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    global_score = Column(
        Integer, CheckConstraint("global_score BETWEEN 0 AND 100", name="ck_score_range")
    )
    scores_detail = Column(JSONB)
    scored_at = Column(DateTime(timezone=True))
    alert_sent = Column(Boolean, default=False)
    __table_args__ = (
        Index("ix_application_job_posting_id", "job_posting_id"),
        Index("ix_application_stage", "stage"),
        Index("ix_application_global_score", "global_score"),
        Index("ix_application_submitted_at", "submitted_at"),
    )
    job_posting = relationship("JobPosting", back_populates="applications")
    resume_file = relationship(
        "ResumeFile", back_populates="application", uselist=False, cascade="all, delete-orphan"
    )
    resume_extraction = relationship(
        "ResumeExtraction",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )
    parsing_jobs = relationship(
        "ParsingJob", back_populates="application", cascade="all, delete-orphan"
    )
    action_logs = relationship(
        "ActionLog", back_populates="application", cascade="all, delete-orphan"
    )
    internal_notes = relationship(
        "InternalNote", back_populates="application", cascade="all, delete-orphan"
    )
    email_logs = relationship(
        "EmailLog", back_populates="application", cascade="all, delete-orphan"
    )


class ResumeFile(Base):
    __tablename__ = "resume_file"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("application.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    file_path = Column(String(500), nullable=False)
    original_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    application = relationship("Application", back_populates="resume_file")


class ResumeExtraction(Base):
    __tablename__ = "resume_extraction"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey("application.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    extracted_name = Column(String(255))
    extracted_email = Column(String(255))
    skills = Column(JSONB)
    years_of_experience = Column(Integer, default=0)
    education_level = Column(Enum(EducationLevel), default=EducationLevel.not_specified)
    parsing_status = Column(Enum(ParsingStatus), nullable=False, default=ParsingStatus.pending)
    extracted_at = Column(DateTime(timezone=True))
    attempt_count = Column(Integer, default=0)
    application = relationship("Application", back_populates="resume_extraction")


class ParsingJob(Base):
    __tablename__ = "parsing_job"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(
        UUID(as_uuid=True), ForeignKey("application.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(Enum(ParsingStatus), nullable=False, default=ParsingStatus.pending)
    attempt_count = Column(Integer, nullable=False, default=0)
    last_error = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    application = relationship("Application", back_populates="parsing_jobs")
