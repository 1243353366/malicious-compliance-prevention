from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "malicious-compliance-prevention"
    app_env: str = "development"
    database_url: str = Field(..., alias="DATABASE_URL")
    secret_key: str = Field(..., alias="SECRET_KEY")
    upload_max_bytes: int = 15 * 1024 * 1024
    allowed_extensions: str = ".txt,.pdf,.docx"
    ocr_enabled: bool = False

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


settings = Settings()
