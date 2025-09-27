from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import User, OAuthAccount
from app.schemas import UserCreate
from app.auth import get_password_hash


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        company_name=user.company_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_oauth_account(db: Session, provider: str, provider_id: str) -> Optional[OAuthAccount]:
    """Get OAuth account by provider and provider ID"""
    return db.query(OAuthAccount).filter(
        and_(OAuthAccount.provider == provider, OAuthAccount.provider_id == provider_id)
    ).first()


def create_oauth_account(
    db: Session, 
    user_id: str, 
    provider: str, 
    provider_id: str, 
    access_token: Optional[str] = None
) -> OAuthAccount:
    """Create OAuth account"""
    oauth_account = OAuthAccount(
        user_id=user_id,
        provider=provider,
        provider_id=provider_id,
        access_token=access_token
    )
    db.add(oauth_account)
    db.commit()
    db.refresh(oauth_account)
    return oauth_account


def create_oauth_user(
    db: Session, 
    email: str, 
    first_name: str, 
    last_name: str, 
    company_name: str,
    provider: str,
    provider_id: str,
    access_token: Optional[str] = None
) -> User:
    """Create user from OAuth data"""
    # Create user without password
    db_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        company_name=company_name,
        is_verified=True  # OAuth users are considered verified
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create OAuth account
    create_oauth_account(db, str(db_user.id), provider, provider_id, access_token)
    
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.password_hash:
        return None  # User registered via OAuth
    
    from app.auth import verify_password
    if not verify_password(password, user.password_hash):
        return None
    return user
