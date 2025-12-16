from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    DEFAULT_THEME: str = "claro"
    DEFAULT_REVISION_INTERVAL: str = "1,7,14"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    class Config:
        env_file = "../.env"

settings = Settings()
