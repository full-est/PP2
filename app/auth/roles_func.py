from fastapi import HTTPException, Depends
from app.auth.auth import get_current_user
from app.models import User

def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return current_user
