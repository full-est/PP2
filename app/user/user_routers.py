from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.models import User
from app.schemas import UserResponse, UserUpdate
from app.database import get_db

users = APIRouter(
    tags=["user"],
    dependencies=[Depends(get_current_user)]
)

def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Для получения данных о текущем пользователе
@users.get("/users/me", response_model= UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Позволяет видеть всех зарегистрированных пользователей.
@users.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# Для просмотра данных конкретного пользователя.
@users.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)
    return user

# Изменение данных(username) у пользователя.
@users.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    user = get_user_by_id(current_user.id, db)

    user.username = user_update.username
    db.commit()
    db.refresh(user)
    return user

@users.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not (user_id == current_user.id or current_user.role == "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to delete users")
    user = get_user_by_id(user_id, db)

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
