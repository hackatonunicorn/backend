from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, Field
import uuid


# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    company_name: str = Field(..., min_length=2, max_length=255)
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v.replace(' ', '').replace('-', '').replace("'", '').isalpha():
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        return v.title()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    agree_terms: bool = Field(..., description="Must agree to terms and conditions")
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('agree_terms')
    def validate_terms_agreement(cls, v):
        if not v:
            raise ValueError('You must agree to the terms and conditions')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class UserResponse(UserBase):
    id: uuid.UUID
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfile(UserResponse):
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Auth schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    user_id: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RegisterResponse(BaseModel):
    message: str
    user: UserResponse


# OAuth schemas
class OAuthLogin(BaseModel):
    token: str


# Error schemas
class ValidationErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    detail: str | list[ValidationErrorDetail]
