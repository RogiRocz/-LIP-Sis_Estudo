import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", ".env")
)
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DEFAULT_THEME: str = "claro"
    DEFAULT_REVISION_INTERVAL: list[int] = [1, 7, 14]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEFAULT_TIMEZONE: str = "America/Sao_Paulo"

    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str


settings = Settings()
