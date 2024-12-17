from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.models import ProjectMember, User, Project
from app.schemas import ProjectMemberResponse, UserResponse
from app.database import get_db

member = APIRouter(
    tags=["project_member"]
)

@member.get("/{project_id}/members", response_model=list[UserResponse])
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    # Проверяем существование проекта
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Проверяем, имеет ли пользователь доступ к проекту
    project_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()
    if not project_member:
        raise HTTPException(status_code=403, detail="Not authorized for this project")

    # Получаем список участников
    members = (
        db.query(User)
        .join(ProjectMember, ProjectMember.user_id == User.id)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )
    return members

# Добавление пользователя в проект
@member.post("/{project_id}/members", response_model=ProjectMemberResponse)
def add_project_member(project_id: int,
                       user_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    # Проверяем, существует ли проект
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Только владелец проекта может добавлять участников
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add members to this project")

    # Проверяем, что пользователь уже не является участником
    existing_member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of this project")

    # Добавляем нового участника
    new_member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role="member"
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

# Удаление пользователя из проекта
@member.delete("/{project_id}/members/{user_id}")
def remove_project_member(project_id: int,
                          user_id: int,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    # Проверяем, существует ли проект
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Только владелец проекта может удалять участников
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to remove members from this project")

    if user_id == current_user.id:
        raise HTTPException(status_code=403, detail="You can't remove yourself from project")

    # Ищем участника
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Удаляем участника
    db.delete(member)
    db.commit()
    return {"message": f"User with ID {user_id} removed from project {project_id}"}

