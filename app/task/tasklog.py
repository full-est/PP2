from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session, joinedload
from app.auth.auth import get_current_user
from app.database import get_db
from app.schemas import TaskLogResponse
from app.models import TaskLog, User, Task, ProjectMember, Project

tasklog = APIRouter(
    tags=["tasklog"]
)


def create_task_log(task_id: int, project_id: int, user_id: int, message: str, db: Session):

    log_entry = TaskLog(
        task_id=task_id,
        project_id=project_id,
        user_id=user_id,
        message=message,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

# Получение логов задачи
@tasklog.get("/tasks/{task_id}/logs", response_model=list[TaskLogResponse])
def get_task_logs(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Проверяем существование задачи
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    project_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == task.columns.project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not project_member:
        raise HTTPException(status_code=404, detail="Not authorized to delete this task")

    logs = db.query(TaskLog).filter(TaskLog.task_id == task_id).all()
    return logs

@tasklog.get("/projects/{project_id}/logs")
def get_project_task_logs(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_logs = (
        db.query(TaskLog)
        .options(joinedload(TaskLog.task))  # Подгрузка связанных задач
        .filter(TaskLog.project_id == project_id)
        .all()
    )

    return project_logs
