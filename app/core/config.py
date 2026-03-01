from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    PROJECT_NAME: str = "TODO API"
    VERSION: str = "0.1.0"

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "todo_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
