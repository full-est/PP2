from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Project, User, ProjectMember
from schemas import ProjectResponse, ProjectCreate, ProjectUpdate
from database import get_db

project_router = APIRouter(
    tags=["project"]
)

# Создает новый проект. Здесь задается owner_id (владелец проекта).
@project_router.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == project.owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=project.owner_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

    # Получаем все проекты
@project_router.get("/projects", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

    # Ищем проект по ID
@project_router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

    # Обновляем проект
@project_router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.name = project_update.name or project.name
    project.description = project_update.description or project.description
    project.owner_id = project.owner_id
    db.commit()
    db.refresh(project)
    return project

# Удаляет проект и связанные данные (колонки, задачи, участников).
@project_router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully"}

