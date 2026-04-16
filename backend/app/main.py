from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import engine
from app.features.applications.router import router as applications_router
from app.features.auth.router import router as auth_router
from app.features.emails.router import router as emails_router
from app.features.export.router import router as export_router
from app.features.jobs.router import router as jobs_router
from app.features.pipeline.router import router as pipeline_router
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.debug:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="ATS Platform API",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(applications_router, prefix="/api/v1/applications", tags=["Applications"])
app.include_router(pipeline_router, prefix="/api/v1/pipeline", tags=["Pipeline"])
app.include_router(emails_router, prefix="/api/v1/emails", tags=["Emails"])
app.include_router(export_router, prefix="/api/v1/export", tags=["Export"])


@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production",
    }


@app.get("/", tags=["System"])
async def root():
    return {"message": "ATS Platform API", "docs": "/docs", "health": "/health"}
