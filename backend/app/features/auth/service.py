from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token, verify_password, blacklist_token
from app.core.config import settings
from app.models import User

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate(self, email: str, password: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user is None or not verify_password(password, user.password_hash):
            return None
        return user

    def generate_token(self, user: User) -> dict:
        expire_minutes = settings.access_token_expire_minutes
        result = create_access_token(
            data={"sub": str(user.id), "role": user.role.value},
            expires_delta=timedelta(minutes=expire_minutes),
        )
        return {
            "access_token": result["token"],
            "jti": result["jti"],
            "expires_in": expire_minutes * 60,
        }

    async def revoke_token(self, jti: str, expires_in: int) -> None:
        """Add token to the blacklist for the remaining validity period."""
        await blacklist_token(jti, expires_in)