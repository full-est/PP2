from typing import Optional
from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.database import get_db
from app.models import Task, Column, User, ProjectMember
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.task.tasklog import create_task_log
from app.columns.column_routers import get_column_by_id, get_column_to_update

task = APIRouter(
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)

def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def get_project_member(db, column, current_user):
    project_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == column.project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    return project_member

# Создание задачи
@task.post("/{project_id}/columns/{column_id}/tasks", response_model=TaskResponse)
def create_task(column_id: int,
                task: TaskCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    column = get_column_to_update(column_id, db, current_user)

    new_task = Task(
        title=task.title,
        description=task.description,
        column_id=column_id,
        status=task.status,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    create_task_log(
        task_id=new_task.id,
        user_id=current_user.id,
        project_id=column.project.id,
        message=f"Task '{new_task.title}' was created.",
        db=db,
    )

    return new_task

# Получение всех задач колонки
@task.get("/{project_id}/columns/{column_id}/tasks", response_model=list[TaskResponse])
def get_tasks(column_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.column_id == column_id).all()
    return tasks

# Обновление задачи
@task.put("/{project_id}/columns/{column_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int,
                task_data: TaskUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    task = get_task_by_id(task_id, db)
    column = get_column_by_id(task.column_id, db)
    project_member = get_project_member(db, column, current_user)


    if not project_member:
        raise HTTPException(status_code=404, detail="Not authorized to update this task")


    task.description = task_data.description or task.description
    task.status = task_data.status or task.status
    task.due_date = task_data.due_date or task.due_date
    task.assigned_to = task_data.assigned_to or task.assigned_to

    db.commit()
    db.refresh(task)

    create_task_log(
        task_id=task.id,
        user_id=current_user.id,
        project_id=column.project.id,
        message=f"Task '{task.title}' was updated.",
        db=db,
    )

    return task

# Удаление задачи
@task.delete("/{project_id}/columns/{column_id}/tasks/{task_id}")
def delete_task(task_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    task = get_task_by_id(task_id, db)

    if task.columns.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add tasks to this column")

    create_task_log(
        task_id=task_id,
        project_id=task.columns.project.id,
        user_id=current_user.id,
        message=f"Task '{task.title}' was deleted.",
        db=db,
    )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

@task.get("/columns/{column_id}/tasks", response_model=list[TaskResponse])
def get_tasks_by_column(
    column_id: int,
    status: Optional[str] = Query(None, description="Filter by task status"),
    assigned_to: Optional[int] = Query(None, description="Filter by assigned user ID"),
    title_contains: Optional[str] = Query(None, description="Filter tasks by title containing this string"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Проверяем существование колонки
    column = get_column_by_id(column_id, db)

    # Проверяем доступ к проекту, связанному с колонкой
    project_member = get_project_member(db, column, current_user)

    if not project_member:
        raise HTTPException(status_code=403, detail="Not authorized for this project")

    # Строим фильтры для задач
    filters = [Task.column_id == column_id]

    if status:
        filters.append(Task.status == status)
    if assigned_to:
        filters.append(Task.assigned_to == assigned_to)
    if title_contains:
        filters.append(Task.title.ilike(f"%{title_contains}%"))

    # Применяем фильтры
    tasks = db.query(Task).filter(and_(*filters)).all()

    return tasks
