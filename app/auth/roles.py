from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.auth.roles_func import is_admin
from app.database import get_db
from app.models import User
from app.schemas import RoleUpdate

roles = APIRouter(
    tags=["roles"]
)

@roles.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(is_admin),  # Только администраторы могут менять роли
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if role_update.role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user.role = role_update.role
    db.commit()
    db.refresh(user)
    return {"detail": f"User {user.username} role updated to {role_update.role}"}
