# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from models import Project, Column
# from schemas import ColumnCreate, ColumnUpdate, ColumnResponse
# from database import get_db
#
# column_router = APIRouter()
#
# @app.post('/projects/{project_id}/column')
# def add_column(project_id: int, column: ColumnCreate, db: Session = Depends(get_db)):
#     existing_project = db.query(Project).filter(Project.id == project_id)
#         if not existing_project:
#             raise HTTPException(status_code=404, detail="Project not found")