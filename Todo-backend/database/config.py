
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/todoapp"
    db_echo_sql: bool = False
    db_pool_size: int = 20
    db_max_overflow: int = 30
    better_auth_secret: str = "your-super-secret-jwt-key-here"

    class Config:
        env_file = ".env"

settings = Settings()