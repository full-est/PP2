from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str
    created_at: datetime
    role: str

class UserCreate(BaseModel):
    username: str
    created_at: datetime
    email: EmailStr
    password: str = Field(..., min_length=1, description="Password must not be empty")

class UserUpdate(BaseModel):
    username: str

class UserResponse(User):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(ProjectCreate):
    name: Optional[str]
    description: Optional[str]

class ProjectResponse(ProjectUpdate):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    owner: UserResponse

    class Config:
        from_attributes = True


class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True

class ColumnCreate(BaseModel):
    name: str
    order: int

class ColumnUpdate(BaseModel):
    name: Optional[str]
    order: Optional[int]

class ColumnResponse(BaseModel):
    id: int
    name: str
    order: int
    project_id: int

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None


class TaskUpdate(BaseModel):
    description: Optional[str]
    status: Optional[str]
    due_date: Optional[datetime]
    assigned_to: Optional[int]


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    column_id: int
    created_at: datetime
    due_date: Optional[datetime]
    assigned_to: Optional[int]

    class Config:
        from_attributes = True

class TaskLogResponse(BaseModel):
    id: int
    task_id: int
    message: str
    created_at: datetime
    user_id: Optional[int]
    task: Optional[TaskResponse]

    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RoleUpdate(BaseModel):
    role: str  # user, admin
