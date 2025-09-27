from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.schemas import (
    UserLogin, UserCreate, LoginResponse, RegisterResponse, 
    OAuthLogin, UserProfile
)
from app.crud import (
    get_user_by_email, create_user, authenticate_user,
    get_oauth_account, create_oauth_user, create_oauth_account
)
from app.auth import create_tokens
from app.dependencies import get_current_active_user
from app.models import User
from app.oauth import verify_oauth_token
from app.config import settings

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
@limiter.limit(f"{settings.rate_limit_requests}/minute")
async def login(request: Request, user_credentials: UserLogin, db: Session = Depends(get_db)):
    """User login with email and password"""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token, refresh_token = create_tokens(str(user.id))
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.access_token_expire_minutes * 60,
        user=user
    )


@router.post("/register", response_model=RegisterResponse)
@limiter.limit(f"{settings.rate_limit_requests}/minute")
async def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    """User registration"""
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{
                "field": "email",
                "message": "Email already registered"
            }]
        )
    
    # Create new user
    user = create_user(db, user_data)
    
    return RegisterResponse(
        message="Account created successfully",
        user=user
    )


@router.post("/google", response_model=LoginResponse)
@limiter.limit(f"{settings.rate_limit_requests}/minute")
async def google_login(request: Request, oauth_data: OAuthLogin, db: Session = Depends(get_db)):
    """Google OAuth login"""
    # Verify Google token
    user_info = await verify_oauth_token("google", oauth_data.token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    
    # Check if OAuth account exists
    oauth_account = get_oauth_account(db, "google", user_info["provider_id"])
    
    if oauth_account:
        # Existing OAuth user
        user = oauth_account.user
    else:
        # Check if user exists with this email
        existing_user = get_user_by_email(db, user_info["email"])
        if existing_user:
            # Link OAuth account to existing user
            create_oauth_account(
                db, 
                str(existing_user.id), 
                "google", 
                user_info["provider_id"], 
                oauth_data.token
            )
            user = existing_user
        else:
            # Create new user from OAuth data
            user = create_oauth_user(
                db,
                user_info["email"],
                user_info["first_name"],
                user_info["last_name"],
                user_info["first_name"] + " " + user_info["last_name"] + " Company",  # Default company name
                "google",
                user_info["provider_id"],
                oauth_data.token
            )
    
    access_token, refresh_token = create_tokens(str(user.id))
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.access_token_expire_minutes * 60,
        user=user
    )


@router.post("/linkedin", response_model=LoginResponse)
@limiter.limit(f"{settings.rate_limit_requests}/minute")
async def linkedin_login(request: Request, oauth_data: OAuthLogin, db: Session = Depends(get_db)):
    """LinkedIn OAuth login"""
    # Verify LinkedIn token
    user_info = await verify_oauth_token("linkedin", oauth_data.token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid LinkedIn token"
        )
    
    # Check if OAuth account exists
    oauth_account = get_oauth_account(db, "linkedin", user_info["provider_id"])
    
    if oauth_account:
        # Existing OAuth user
        user = oauth_account.user
    else:
        # Check if user exists with this email
        existing_user = get_user_by_email(db, user_info["email"])
        if existing_user:
            # Link OAuth account to existing user
            create_oauth_account(
                db, 
                str(existing_user.id), 
                "linkedin", 
                user_info["provider_id"], 
                oauth_data.token
            )
            user = existing_user
        else:
            # Create new user from OAuth data
            user = create_oauth_user(
                db,
                user_info["email"],
                user_info["first_name"],
                user_info["last_name"],
                user_info["first_name"] + " " + user_info["last_name"] + " Company",  # Default company name
                "linkedin",
                user_info["provider_id"],
                oauth_data.token
            )
    
    access_token, refresh_token = create_tokens(str(user.id))
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.access_token_expire_minutes * 60,
        user=user
    )


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user
