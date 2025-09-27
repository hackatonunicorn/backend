import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/unicorn_db"
    database_url_test: str = "postgresql://user:password@localhost:5432/unicorn_db_test"
    
    # JWT
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    
    # OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@unicorn.com"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Environment
    environment: str = "development"
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    port: int = 8000
    
    # Security
    bcrypt_rounds: int = 12
    rate_limit_requests: int = 5
    rate_limit_window: int = 60
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v or ["*"]
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
