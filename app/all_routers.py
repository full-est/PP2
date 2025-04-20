from fastapi import APIRouter
from app.auth.auth import auth
from app.auth.roles import roles
from app.columns.column_routers import column
from app.project.project_routers import projects
from app.project_member.project_member_routers import member
from app.task.routers import task
from app.task.tasklog import tasklog
from app.user.user_routers import users

all_routers = APIRouter()

all_routers.include_router(auth)
all_routers.include_router(roles)
all_routers.include_router(users)
all_routers.include_router(projects)
all_routers.include_router(column)
all_routers.include_router(task)
all_routers.include_router(tasklog)
all_routers.include_router(member)