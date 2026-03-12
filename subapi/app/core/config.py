from functools import lru_cache

from app.app import app
from app.core.settings import Settings, EnvironmentSettings


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_environment_settings() -> EnvironmentSettings:
    settings = get_settings()
    return EnvironmentSettings(_env_file=f".env.{settings.ENVIRONMENT}")


settings = get_environment_settings()
