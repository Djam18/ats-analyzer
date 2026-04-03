# app/models/job.py
import enum
import uuid

from sqlalchemy import (
    CheckConstraint, Column, Enum, ForeignKey,
    Integer, String, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.models.base import Base


class JobStatus(str, enum.Enum):
    draft  = "draft"
    active = "active"
    closed = "closed"
    # archived → V2, retiré du MVP


class JobPosting(Base):
    __tablename__ = "job_posting"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title           = Column(String(255), nullable=False)
    description     = Column(Text, nullable=False)
    location        = Column(String(255), nullable=True)
    contract_type   = Column(String(100), nullable=True)
    status          = Column(Enum(JobStatus), nullable=False, default=JobStatus.draft)
    slug            = Column(String(255), nullable=False, unique=True)
    alert_threshold = Column(Integer, nullable=False, default=80)

    # ✅ Propriétaire de l'offre
    created_by_id   = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    # Relations
    created_by         = relationship("User", back_populates="job_postings")
    scoring_criteria   = relationship("ScoringCriterion", back_populates="job_posting",
                                      cascade="all, delete-orphan")
    required_skills    = relationship("RequiredSkill", back_populates="job_posting",
                                      cascade="all, delete-orphan")
    required_languages = relationship("RequiredLanguage", back_populates="job_posting",
                                      cascade="all, delete-orphan")
    applications       = relationship("Application", back_populates="job_posting",
                                      cascade="all, delete-orphan")


class ScoringCriterion(Base):
    __tablename__ = "scoring_criterion"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_posting_id = Column(UUID(as_uuid=True),
                            ForeignKey("job_posting.id", ondelete="CASCADE"), nullable=False)
    criterion_name = Column(String(50), nullable=False)
    weight         = Column(Integer, nullable=False)  # 0-100

    __table_args__ = (
        # ✅ Validation métier dans l'Enum Python, pas en SQL hardcodé
        CheckConstraint("weight >= 0 AND weight <= 100", name="ck_weight_range"),
        UniqueConstraint("job_posting_id", "criterion_name", name="uq_criterion_per_job"),
    )

    job_posting = relationship("JobPosting", back_populates="scoring_criteria")


class RequiredSkill(Base):
    __tablename__ = "required_skill"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_posting_id = Column(UUID(as_uuid=True),
                            ForeignKey("job_posting.id", ondelete="CASCADE"), nullable=False)
    skill_name     = Column(String(100), nullable=False)

    job_posting = relationship("JobPosting", back_populates="required_skills")


class RequiredLanguage(Base):
    __tablename__ = "required_language"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_posting_id = Column(UUID(as_uuid=True),
                            ForeignKey("job_posting.id", ondelete="CASCADE"), nullable=False)
    language_name  = Column(String(50), nullable=False)

    job_posting = relationship("JobPosting", back_populates="required_languages")