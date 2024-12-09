from fastapi import FastAPI
from database import Base, engine
from user.user_routers import router
from auth.auth import auth
from project.project_routers import project_router
from project_member.project_member_routers import member_router
# from column_routers import column_router

app = FastAPI()
app.include_router(auth)
app.include_router(router)
app.include_router(project_router)
# app.include_router(column_router)
app.include_router(member_router)

Base.metadata.create_all(bind=engine)


# Позволяет пользователю увидеть все проекты, в которых он участвует.


# Позволяет владельцу проекта добавлять других пользователей.

# Убирает участника из проекта.
@app.delete('/projects/{project_id}/members/{member_id}')
def delete_member():
    ...

# Показывает, кто участвует в проекте и какие роли они имеют.
@app.get('/projects/{project_id}/members')
def get_members():
    ...

# Добавляет новую колонку в проект.
@app.post('/projects/{project_id}/column')
def add_column():
    ...

# Возвращает все колонки проекта с их порядком (order).
@app.get('/projects/{project_id}/column')
def get_columns():
    ...

# Позволяет изменить название или порядок колонки.
@app.put('/projects/{project_id}/column/{column_id}')
def update_column():
    ...

# Удаляет колонку вместе с её задачами.
@app.delete('/projects/{project_id}/column/{column_id}')
def delete_column():
    ...

# Создает задачу внутри конкретной колонки.
@app.post('/column/{column_id}/tasks')
def add_task():
    ...

# Возвращает задачи с возможностью фильтрации по статусу, сроку выполнения, исполнителю и т. д.
@app.get('/column/{column_id}/tasks')
def get_all_tasks():
    ...

# Детальная информация о задаче, включая связанные данные (например, пользователь, которому она назначена).
@app.get('/tasks/{task_id}')
def get_task():
    ...

# Позволяет изменять информацию о задаче (например, статус, срок выполнения или исполнителя).
@app.put('/tasks/{task_id}')
def update_task():
    ...

# Удаляет задачу
@app.delete('/projects/{project_id}/column/{column_id}')
def delete_task():
    ...

# Позволяет добавлять сообщение/комментарий к задаче.
@app.post('/tasks/{task_id}/logs')
def add_log():
    ...

# Возвращает историю всех логов для конкретной задачи (например, комментарии или изменения статуса).
@app.get('/tasks/{task_id}/logs')
def get_logs():
    ...
