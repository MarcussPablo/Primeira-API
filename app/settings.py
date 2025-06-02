from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    PROJECT_NAME: str = "My API"

    class Config:
        env_file = ".env"

settings = Settings()
