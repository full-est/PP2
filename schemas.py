from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class User(BaseModel):
    username: str
    created_at: datetime

class UserCreate(User):
    email: EmailStr
    password: str

class UserResponse(User):
    id: UUID
    email: EmailStr

    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime
    owner_id: UUID

    class Config:
        orm_mode = True

class ProjectMemberCreate(BaseModel):
    user_id: UUID
    role: str


class ProjectMemberResponse(BaseModel):
    id: UUID
    project_id: UUID
    user_id: UUID
    role: str
    joined_at: datetime

    class Config:
        orm_mode = True

class ColumnCreate(BaseModel):
    name: str
    order: int

class ColumnUpdate(BaseModel):
    name: Optional[str]
    order: Optional[int]

class ColumnResponse(BaseModel):
    id: UUID
    name: str
    order: int
    project_id: UUID

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    column_id: UUID
    due_date: Optional[datetime] = None
    assigned_to: Optional[UUID] = None


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    column_id: Optional[UUID]
    due_date: Optional[datetime]
    assigned_to: Optional[UUID]


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: str
    column_id: UUID
    created_at: datetime
    due_date: Optional[datetime]
    assigned_to: Optional[UUID]

    class Config:
        orm_mode = True
