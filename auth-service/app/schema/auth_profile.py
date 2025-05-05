from pydantic import BaseModel, EmailStr, Field, validator
from uuid import UUID
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    RIDER = 'RIDER'
    DRIVER = 'DRIVER'
    ADMIN = 'ADMIN'
    
    
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: UserRole = UserRole.RIDER
    
    
class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    

class UserResponse(UserBase):
    uuid: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
        
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserResponse
    

class VerifyEmailRequeest(BaseModel):
    token: str
    
    
class PasswordResetRequest(BaseModel):
    email: EmailStr
    
    
class PasswordResetConfirm(BaseModel):
    new_password: str
    
    @validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password should have aat least 8 characters long')
        return v
    
class ResponseMessage(BaseModel):
    message: str
    success: bool = True