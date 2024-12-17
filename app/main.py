from fastapi import FastAPI
from app.auth.roles import roles
from app.database import Base, engine
from app.user.user_routers import users
from app.auth.auth import auth
from app.project.project_routers import projects
from app.project_member.project_member_routers import member
from app.columns.column_routers import column
from app.task.routers import task
from app.task.tasklog import tasklog

app = FastAPI()
app.include_router(auth)
app.include_router(roles)
app.include_router(users)
app.include_router(projects)
app.include_router(column)
app.include_router(task)
app.include_router(tasklog)
app.include_router(member)

Base.metadata.create_all(bind=engine)