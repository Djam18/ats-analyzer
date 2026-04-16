import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from app.main import app
from app.database import get_db
from app.models.base import Base

# Base de données de test en mémoire (SQLite pour la rapidité)
# Pour PostgreSQL, on peut utiliser un conteneur Docker, mais SQLite suffit pour les tests unitaires.
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
async def db_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Fixture pour un utilisateur recruteur (authentifié)
@pytest.fixture
async def auth_headers():
    # À implémenter si vous avez un endpoint de login
    # Pour les tests, on peut contourner l’auth en créant un utilisateur et en générant un token JWT.
    # En attendant, on peut utiliser un fixture qui crée un utilisateur et retourne les headers.
    # Pour simplifier, nous allons d’abord tester sans auth (à adapter selon votre code).
    # Je vous propose de créer un utilisateur de test et de générer un token.
    # Exemple :
    from app.models.user import User
    from app.core.security import create_access_token
    async with TestingSessionLocal() as session:
        user = User(email="test@example.com", nom="Test User", mot_de_passe_hash="fake")
        session.add(user)
        await session.commit()
        token = create_access_token({"sub": str(user.id)})
        return {"Authorization": f"Bearer {token}"}
    # Pour l’instant, retournez un dict vide si l’auth est désactivée en test
    return {}