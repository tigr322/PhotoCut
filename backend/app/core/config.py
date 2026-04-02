from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "PhotoCut"
    api_v1_prefix: str = "/api/v1"

    secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 24 * 60

    database_url: str = "postgresql+psycopg2://photocut:photocut@postgres:5432/photocut"
    redis_url: str = "redis://redis:6379/0"
    rq_queue: str = "image_jobs"

    storage_root: str = "/app/data"
    max_upload_size_mb: int = 10

    api_key_pepper: str = "change-me-too"

    cors_origins: list[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
