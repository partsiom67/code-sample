import json
from datetime import timedelta
from enum import Enum
from typing import List
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class SourceType(str, Enum):
    FETCH = "fetch"
    SUBSCRIBE = "subscribe"


class Source(BaseModel):
    name: str
    type: SourceType
    url: str


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class EnvironmentSettings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    DATABASE_NAME: str
    ITEMS_LIMIT: int
    INTERVAL: int
    TIMEOUT: int
    MAX_RETRIES: int
    RETRY_DELAY: int
    SOURCES_FILE: str = "sources.json"
    SOURCES: List[Source] = []
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(days=1)
    REFRESH_TOKEN_LIFETIME: timedelta = timedelta(days=7)

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file="",
        env_file_encoding="utf-8",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_sources()

    def load_sources(self):
        sources_path = Path(self.SOURCES_FILE)
        if sources_path.exists():
            with open(sources_path) as f:
                self.SOURCES = json.load(f)
