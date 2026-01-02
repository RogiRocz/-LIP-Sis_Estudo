import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", ".env")
)
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    DEFAULT_THEME: str = "claro"
    DEFAULT_REVISION_INTERVAL: str = "1,7,14"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
