from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List

from app.models import User, UserRole
from app.schema import UserCreate, UserUpdate
from app.security import get_password_hash, verify_password



def get_user_by_uuid(db: Session, uuid: str):
    return db.query(User).filter(User.uuid == uuid).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_phonenumber(db: Session, phone_number: str):
    return db.query(User).filter(User.phone_number == phone_number).first()


def create_user(db: Session, user: UserCreate):
    db_user_email = get_user_by_email(db, email=user.email)
    db_user_phone = get_user_by_phonenumber(db, phone_number=user.phone_number)   
    
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Email already in use'
        )
    if db_user_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Phone number already in use'
        )
        
    hashed_password = get_password_hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        password_hash=hashed_password,
        role=user.role
    ) 
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Error creating the user'
        )
        
        
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user