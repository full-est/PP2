from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str
    created_at: datetime

class UserCreate(User):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: str

class UserResponse(User):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int

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

class ProjectMemberCreate(BaseModel):
    user_id: int
    role: str


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
    column_id: int
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    column_id: Optional[int]
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
