from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from authx import AuthX, AuthXConfig
from auth.auth import get_current_user
from models import User
from schemas import UserCreate, UserResponse, UserUpdate, UserLogin
from database import get_db

router = APIRouter(
    tags=["user"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

# Позволяет видеть всех зарегистрированных пользователей.
@router.get("/users", response_model=UserResponse)
def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# Для проверки данных конкретного пользователя.
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Изменение данных(username) у пользователя.
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    # Проверяем, что пользователь обновляет свои данные
    if current_user.username != user_id:
        raise HTTPException(status_code=403, detail="You can update only your data")

    user = db.query(User).filter(User.username == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_update.username
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
def delete_user(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
