from app.models import Column, Project, User
from app.schemas import ColumnCreate, ColumnUpdate, ColumnResponse
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.database import get_db

column = APIRouter(
    tags=["columns"]
)
# Создание колонки
@column.post("/{project_id}/columns", response_model=ColumnResponse)
def create_column(project_id: int, 
                  column: ColumnCreate, 
                  db: Session = Depends(get_db), 
                  current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add columns to this project")

    new_column = Column(
        name=column.name,
        project_id=project_id,
        order=column.order
    )
    db.add(new_column)
    db.commit()
    db.refresh(new_column)
    return new_column

# Получение всех колонок проекта
@column.get("/{project_id}/columns", response_model=list[ColumnResponse])
def get_columns(project_id: int, db: Session = Depends(get_db), 
                current_user: User = Depends(get_current_user)):
    columns = db.query(Column).filter(Column.project_id == project_id).all()
    return columns

# Обновление колонки
@column.put("/{project_id}/columns/{column_id}", response_model=ColumnResponse)
def update_column(column_id: int,
                  column_data: ColumnUpdate, 
                  db: Session = Depends(get_db), 
                  current_user: User = Depends(get_current_user)):

    column = db.query(Column).filter(Column.id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    if column.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this column")
    column.name = column_data.name
    column.order = column_data.order
    db.commit()
    db.refresh(column)
    return column

# Удаление колонки
@column.delete("/{project_id}/columns/{column_id}")
def delete_column(column_id: int,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    column = db.query(Column).filter(Column.id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    if column.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this column")

    db.delete(column)
    db.commit()
    return {"message": "Column deleted successfully"}
