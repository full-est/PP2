from sqlalchemy import Column, String, Text, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False)
    column_id = Column(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    due_date = Column(TIMESTAMP, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    columns = relationship("Column", back_populates="tasks")
    assigned_user = relationship("User", foreign_keys=[assigned_to])
    logs = relationship("TaskLog", back_populates="task")

class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    task = relationship("Task", back_populates="logs")
    user = relationship("User", foreign_keys=[user_id])
    project = relationship("Project", back_populates="logs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)  # Хэшированный пароль
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    role = Column(String(20), default="user") # user, admin

    projects_owned = relationship("Project", back_populates="owner", cascade="all, delete")
    project_memberships = relationship("ProjectMember", back_populates="user")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="projects_owned")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete")
    columns = relationship("Column", back_populates="project", cascade="all, delete")
    logs = relationship("TaskLog", back_populates="project", cascade="all, delete")

class ProjectMember(Base):
    __tablename__ = "project_member"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False) # owner, member
    joined_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")

class Column(Base):
    __tablename__ = "columns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    order = Column(Integer, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    project = relationship("Project", back_populates="columns")
    tasks = relationship("Task", back_populates="columns", cascade="all, delete")
