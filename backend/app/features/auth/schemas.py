import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="recruiter@ats.dev")
    password: str = Field(..., min_length=6, example="recruiter1234")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token lifetime in seconds")


class UserMeResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime
    model_config = {"from_attributes": True}
