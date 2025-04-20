from app.models import Column, Project, User
from app.schemas import ColumnCreate, ColumnUpdate, ColumnResponse
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.database import get_db
from app.project.project_routers import get_project_by_id

column = APIRouter(
    tags=["columns"],
    dependencies=[Depends(get_current_user)]
)

def get_column_by_id(column_id: int, db: Session = Depends(get_db)):
    column = db.query(Column).filter(Column.id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column

def get_column_to_update(column_id: int, db, current_user):
    column = get_column_by_id(column_id, db)
    if column.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update and delete this column")
    return column

# Создание колонки
@column.post("/{project_id}/columns", response_model=ColumnResponse)
def create_column(project_id: int, 
                  column: ColumnCreate, 
                  db: Session = Depends(get_db), 
                  current_user: User = Depends(get_current_user)):

    project = get_project_by_id(project_id, db)
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
def get_columns(project_id: int, db: Session = Depends(get_db)):
    columns = db.query(Column).filter(Column.project_id == project_id).all()
    return columns

@column.get("/{project_id}/columns/{column_id}", response_model=ColumnResponse)
def get_column(column_id: int, db: Session = Depends(get_db)):
    column = get_column_by_id(column_id, db)
    return column

# Обновление колонки
@column.put("/{project_id}/columns/{column_id}", response_model=ColumnResponse)
def update_column(column_id: int,
                  column_data: ColumnUpdate, 
                  db: Session = Depends(get_db), 
                  current_user: User = Depends(get_current_user)):

    column = get_column_to_update(column_id, db, current_user)

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

    column = get_column_to_update(column_id, db, current_user)

    db.delete(column)
    db.commit()
    return {"message": "Column deleted successfully"}
