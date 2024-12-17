from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Project, User, ProjectMember
from app.schemas import ProjectResponse, ProjectCreate, ProjectUpdate
from app.database import get_db
from app.auth.auth import get_current_user

projects = APIRouter(
    tags=["project"]
)

# Создает новый проект
@projects.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    owner_member = ProjectMember(
        project_id=new_project.id,
        user_id=current_user.id,
        role="owner"
    )

    db.add(owner_member)
    db.commit()

    return new_project

# Получаем все проекты
@projects.get("/projects", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

# Ищем проект по ID
@projects.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Получение всех проектов, в которых пользователь является участником
@projects.get("/users/me/projects", response_model=list[ProjectResponse])
def get_user_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    owned_projects = db.query(Project).filter(Project.owner_id == current_user.id).all()

    member_projects = (
        db.query(Project)
        .join(ProjectMember, Project.id == ProjectMember.project_id)
        .filter(ProjectMember.user_id == current_user.id)
        .all()
    )

    projects = list({project.id: project for project in owned_projects + member_projects}.values())
    return projects

# Обновляем проект
@projects.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int,
                   project_data: ProjectUpdate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this project")
    project.name = project_data.name
    project.description = project_data.description
    db.commit()
    db.refresh(project)
    return project

# Удаляет проект и связанные данные (колонки, задачи, участников).
@projects.delete("/projects/{project_id}")
def delete_project(project_id: int,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}
