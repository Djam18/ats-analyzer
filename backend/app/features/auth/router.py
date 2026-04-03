from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.core.config import settings
from app.core.dependencies import get_current_user
from app.database import get_db
from app.features.auth.schemas import LoginRequest, TokenResponse, UserMeResponse
from app.features.auth.service import AuthService
from app.models import User

router = APIRouter()
bearer_scheme = HTTPBearer()

@router.post("/login", response_model=TokenResponse, status_code=200,
             summary="Authenticate and get a JWT token")
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.authenticate(body.email, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(**service.generate_token(user))

@router.post("/logout", status_code=204, summary="Logout — revoke JWT")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Revoke JWT by adding it to the blacklist.
    Token is invalidated immediately, even before its expiration.
    """
    token = credentials.credentials
    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm]
    )
    jti = payload.get("jti")
    exp = payload.get("exp")

    if jti and exp:
        import time
        remaining_ttl = int(exp - time.time())
        if remaining_ttl > 0:
            await AuthService(db).revoke_token(jti, remaining_ttl)

    return None

@router.get("/me", response_model=UserMeResponse, status_code=200,
            summary="Get authenticated user profile")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user