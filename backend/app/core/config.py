from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    app_version: str = "0.1.0"
    database_url: str = "postgresql+asyncpg://ats:devpass@localhost:5432/ats_dev"
    redis_url: str = "redis://redis:6379"
    parsing_queue: str = "parsing_jobs"
    email_queue: str = "email_jobs"
    secret_key: str = "dev_secret_key_unsafe_do_not_use_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"
    aws_access_key_id: str = "minioadmin"
    aws_secret_access_key: str = "minioadmin"
    aws_s3_endpoint_url: str = "http://minio:9000"
    aws_s3_bucket: str = "ats-cv-local"
    aws_region: str = "eu-west-3"
    s3_signed_url_expiry: int = 3600
    smtp_host: str = "mailhog"
    smtp_port: int = 1025
    smtp_from: str = "noreply@ats-local.dev"
    smtp_tls: bool = False
    parsing_timeout: int = 30
    parsing_max_retries: int = 3

    @property
    def allowed_origins_list(self) -> list[str]:
        return self.allowed_origins.split(",")

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
