import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/unicorn_db"
    database_url_test: str = "postgresql://user:password@localhost:5432/unicorn_db_test"
    
    @property
    def safe_database_url(self) -> str:
        """Get database URL with fallback for Railway"""
        if self.database_url.startswith("postgresql://") and "localhost" not in self.database_url:
            return self.database_url
        # Fallback to environment variable for Railway
        import os
        return os.getenv("DATABASE_URL", self.database_url)
    
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
    cors_origins: str = "http://localhost:3000,http://localhost:3001,https://localhost:3000,https://localhost:3001"
    port: int = 8000
    
    # Security
    bcrypt_rounds: int = 12
    rate_limit_requests: int = 5
    rate_limit_window: int = 60
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string to list"""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins or ["*"]
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
