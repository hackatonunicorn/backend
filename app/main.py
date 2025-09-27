from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.config import settings
from app.routers import auth
from app.database import engine
from app.models import Base
from app.exceptions import validation_exception_handler, http_exception_handler

# Create database tables (only if database is available)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")
    print("This might be normal if DATABASE_URL is not set or database is not available")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="Unicorn Authentication API",
    description="Authentication backend for Unicorn fundraising platform",
    version="1.0.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add custom exception handlers
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["authentication"]
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Test database connection
    db_status = "unknown"
    try:
        from app.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)[:100]}"
    
    return {
        "status": "healthy", 
        "service": "unicorn-auth-api",
        "database": db_status,
        "environment": settings.environment
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Unicorn Authentication API",
        "version": "1.0.0",
        "docs": "/docs" if not settings.is_production else "disabled",
        "environment": settings.environment
    }
