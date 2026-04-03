# app/features/jobs/schemas.py
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, model_validator

# ─── Critères de scoring ────────────────────────────────────────────

VALID_CRITERIA = {"skills", "experience", "education", "languages"}

class ScoringCriterionIn(BaseModel):
    criterion_name: str = Field(..., examples=["skills"])
    weight: int         = Field(..., ge=0, le=100)

    @model_validator(mode="after")
    def check_criterion_name(self):
        if self.criterion_name not in VALID_CRITERIA:
            raise ValueError(f"criterion_name must be one of {VALID_CRITERIA}")
        return self

class ScoringCriterionOut(BaseModel):
    id:             uuid.UUID
    criterion_name: str
    weight:         int
    model_config = {"from_attributes": True}

# ─── Skills & Languages ─────────────────────────────────────────────

class SkillIn(BaseModel):
    skill_name: str = Field(..., min_length=1, max_length=100)

class SkillOut(BaseModel):
    id:         uuid.UUID
    skill_name: str
    model_config = {"from_attributes": True}

class LanguageIn(BaseModel):
    language_name: str = Field(..., min_length=1, max_length=50)

class LanguageOut(BaseModel):
    id:            uuid.UUID
    language_name: str
    model_config = {"from_attributes": True}

# ─── Job Posting ────────────────────────────────────────────────────

class JobCreate(BaseModel):
    title:           str = Field(..., min_length=3, max_length=255)
    description:     str = Field(..., min_length=10)
    location:        Optional[str] = Field(None, max_length=255)
    contract_type:   Optional[str] = Field(None, max_length=100)
    alert_threshold: int           = Field(80, ge=0, le=100)
    scoring_criteria:   list[ScoringCriterionIn] = Field(default_factory=list)
    required_skills:    list[SkillIn]            = Field(default_factory=list)
    required_languages: list[LanguageIn]         = Field(default_factory=list)
    created_by_id:    Optional[uuid.UUID]      = None  # Ignoré à la création, rempli par le service

    @model_validator(mode="after")
    def check_scoring_weights(self):
        criteria = self.scoring_criteria
        if not criteria:
            return self
        # Noms uniques
        names = [c.criterion_name for c in criteria]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate criterion_name in scoring_criteria")
        # Somme = 100
        total = sum(c.weight for c in criteria)
        if total != 100:
            raise ValueError(f"Scoring criteria weights must sum to 100, got {total}")
        return self


class JobUpdate(BaseModel):
    """Tous les champs sont optionnels — PATCH sémantique."""
    title:           Optional[str] = Field(None, min_length=3, max_length=255)
    description:     Optional[str] = Field(None, min_length=10)
    location:        Optional[str] = Field(None, max_length=255)
    contract_type:   Optional[str] = Field(None, max_length=100)
    alert_threshold: Optional[int] = Field(None, ge=0, le=100)
    scoring_criteria:   Optional[list[ScoringCriterionIn]] = None
    required_skills:    Optional[list[SkillIn]]            = None
    required_languages: Optional[list[LanguageIn]]         = None

    @model_validator(mode="after")
    def check_scoring_weights(self):
        criteria = self.scoring_criteria
        if criteria is None:
            return self
        names = [c.criterion_name for c in criteria]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate criterion_name in scoring_criteria")
        total = sum(c.weight for c in criteria)
        if total != 100:
            raise ValueError(f"Scoring criteria weights must sum to 100, got {total}")
        return self


class JobOut(BaseModel):
    id:              uuid.UUID
    title:           str
    description:     str
    location:        Optional[str]
    contract_type:   Optional[str]
    status:          str
    slug:            str
    alert_threshold: int
    created_at:      datetime
    updated_at:      datetime
    scoring_criteria:   list[ScoringCriterionOut]
    required_skills:    list[SkillOut]
    required_languages: list[LanguageOut]
    model_config = {"from_attributes": True}


class JobListOut(BaseModel):
    """Vue allégée pour les listes — pas de description complète."""
    id:            uuid.UUID
    title:         str
    location:      Optional[str]
    contract_type: Optional[str]
    status:        str
    slug:          str
    created_at:    datetime
    model_config = {"from_attributes": True}