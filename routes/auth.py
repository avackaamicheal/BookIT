from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user import User, UserCreate
from database import get_db
from crud.crud_user import user_service
from security import (
    verify_password, 
    create_access_token, 
    create_refresh_token, 
    get_current_user,
    decode_token
)

router = APIRouter()

@router.post("/register", response_model=User, tags=["auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    try:
        created_user=user_service.create_user(db=db, user=user)
        db.commit()
        return created_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", tags=["auth"])
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_service.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(sub=user.email, roles=[user.role.value if hasattr(user.role, 'value') else user.role])
    refresh_token = create_refresh_token(sub=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/token/refresh", tags=["auth"])
def refresh_token(current_user: User = Depends(get_current_user)):
    access_token = create_access_token(sub=current_user.email, roles=[current_user.role.value if hasattr(current_user.role, 'value') else current_user.role])
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User, tags=["users"])
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
