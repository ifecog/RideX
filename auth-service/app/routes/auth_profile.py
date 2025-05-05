from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.schema import auth_profile as user_schema
from app.crud.auth_profile import create_user, get_user_by_email, authenticate_user
from app.security import verify_password
from app.auth import create_access_token
from app.dependencies import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/signup", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return new_user


@router.post("/signin", response_model=user_schema.TokenResponse)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": str(user.email)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }