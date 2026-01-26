from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    db_echo_sql: bool = False
    db_pool_size: int = 20
    db_max_overflow: int = 30
    better_auth_secret: str = "your-super-secret-jwt-key-here"
    next_public_api_base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()