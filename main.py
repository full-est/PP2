from fastapi import FastAPI

app = FastAPI()

# Позволяет создавать новых пользователей.
@app.post('/users')
def add_user():
    ...

# Позволяет видеть всех зарегистрированных пользователей.
@app.get('/users')
def get_all_users():
    ...

# Для проверки данных конкретного пользователя.
@app.get('/users/{user_id}')
def get_user():
    ...

@app.delete('/users/{user_id}')
def delete_user():
    ...

# Создает новый проект. Здесь задается owner_id (владелец проекта).
@app.post('/projects')
def add_project():
    ...

# Позволяет пользователю увидеть все проекты, в которых он участвует.
@app.get('/projects')
def get_all_projects():
    ...

# Детальная информация о проекте.
@app.get('/projects/{project_id}')
def get_project():
    ...

# Позволяет изменять название или описание проекта.
@app.put('/projects/{project_id}')
def update_project():
    ...

# Удаляет проект и связанные данные (колонки, задачи, участников).
@app.delete('/projects/{project_id}')
def delete_project():
    ...

# Позволяет владельцу проекта добавлять других пользователей.
@app.post('/projects/{project_id}/members')
def add_member():
    ...

# Убирает участника из проекта.
@app.delete('/projects/{project_id}/members/{member_id}')
def delete_member():
    ...

# Показывает, кто участвует в проекте и какие роли они имеют.
@app.get('/projects/{project_id}/members')
def get_members():
    ...

# Добавляет новую колонку в проект.
@app.post('/projects/{project_id}/columns')
def add_column():
    ...

# Возвращает все колонки проекта с их порядком (order).
@app.get('/projects/{project_id}/columns')
def get_columns():
    ...

# Позволяет изменить название или порядок колонки.
@app.put('/projects/{project_id}/columns/{column_id}')
def update_column():
    ...

# Удаляет колонку вместе с её задачами.
@app.delete('/projects/{project_id}/columns/{column_id}')
def delete_column():
    ...

# Создает задачу внутри конкретной колонки.
@app.post('/columns/{column_id}/tasks')
def add_task():
    ...

# Возвращает задачи с возможностью фильтрации по статусу, сроку выполнения, исполнителю и т. д.
@app.get('/columns/{column_id}/tasks')
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
@app.delete('/projects/{project_id}/columns/{column_id}')
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
