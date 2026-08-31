"""
Core Application Configuration Settings.
"""

import os
from pathlib import Path
from typing import List, Union
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "SIH26001 Landslide Early-Warning Backend API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Base Directory paths
    BACKEND_DIR: Path = Path(__file__).resolve().parent.parent.parent
    ROOT_DIR: Path = BACKEND_DIR.parent
    AI_MODEL_DIR: Path = ROOT_DIR / "ai" / "saved_models"

    # Database connection URL (defaults to local SQLite, supports PostgreSQL/PostGIS)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./landslide_system.db")

    # CORS Allowed Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]


settings = Settings()
