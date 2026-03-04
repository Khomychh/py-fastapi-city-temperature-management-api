from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City temperature management api"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./db.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
