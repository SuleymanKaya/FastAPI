import os
import secrets
from enum import Enum
from typing import List, Union

from environs import Env
from pydantic import AnyHttpUrl
from pydantic import BaseSettings as PydanticSettings
from slugify import slugify

env = Env()


class SettingsBase(PydanticSettings):
    ROOT_DIR = os.path.abspath(os.path.dirname("src"))

    if env.bool("READ_ENV", default=True):
        env.read_env(f"{ROOT_DIR}/.env")

    # Base settings
    # --------------------------------------------------------------------------
    PROJECT_NAME: str = env.str("PROJECT_NAME", "Project_Example")
    PROJECT_NAME_SLUG: str = slugify(PROJECT_NAME)
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DEBUG: bool = env.bool("DEBUG", False)

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = env.list(
        "BACKEND_CORS_ORIGINS", ["http://127.0.0.1:8000/"]
    )

    # API settings
    # --------------------------------------------------------------------------
    API: str = "/api"
    DEFAULT_OFFSET: int = 0  # default offset of items
    DEFAULT_LIMIT: int = env.int("DEFAULT_LIMIT", 25)  # default limit of items

    # Postgres settings
    # --------------------------------------------------------------------------
    PSQL_HOST: str = env.str("POSTGRES_HOST")
    PSQL_PORT: int = env.int("POSTGRES_PORT")
    PSQL_USER: str = env.str("POSTGRES_USER")
    PSQL_PASSWORD: str = env.str("POSTGRES_PASSWORD")
    PSQL_DB: str = env.str("POSTGRES_DB")
    PSQL_DB_URL: str = (
        f"postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DB}"
    )

    # Logging
    # --------------------------------------------------------------------------
    JSON_LOGS: bool = env.bool("JSON_LOGS", False)


class SettingsLocal(SettingsBase):
    pass


class SettingsTest(SettingsBase):
    pass


class SettingsProd(SettingsBase):
    DEBUG: bool = False


class LaunchMode(str, Enum):
    LOCAL = "local"
    PRODUCTION = "prod"
    TEST = "test"


LAUNCH_MODE = os.environ.get("LAUNCH_MODE")

SettingsType = Union[SettingsLocal, SettingsTest, SettingsProd]


def _get_settings() -> SettingsType:
    if LAUNCH_MODE == LaunchMode.LOCAL.value:
        settings_class = SettingsLocal  # type: ignore
    elif LAUNCH_MODE == LaunchMode.TEST.value:
        settings_class = SettingsTest  # type: ignore
    else:
        settings_class = SettingsProd  # type: ignore
    return settings_class()


settings = _get_settings()
