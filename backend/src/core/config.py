import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", ".env")
)
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DEFAULT_THEME: str = "light"
    DEFAULT_REVISION_INTERVAL: list[int] = [1, 7, 14]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DEFAULT_TIMEZONE: str = "America/Sao_Paulo"
    REFRESH_TOKEN_ROTATION: bool = True

    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str
    SUPABASE_JWT_LEGACY: str

    class Config:
        env_file = env_path


settings = Settings()
