
## Запуск проекта

Проект можно запустить двумя способами: 

1. **С использованием Docker** (рекомендуется).
2. **Без использования Docker** (локально на вашей машине).

### 1. Запуск с использованием Docker

#### Предварительные требования

- Установленный [Docker](https://www.docker.com/).
- Установленный [Docker Compose](https://docs.docker.com/compose/).

#### Шаги:

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/full-est/PP2.git
    cd ваш_репозиторий 
    ```

2. Создайте файл `.env` в корне проекта и добавьте следующие переменные:

    ```env
    DATABASE_URL=postgresql+psycopg://postgres:password@db:5432/yourdatabase
    SECRET_KEY=your-secret-key
    ```

3. Постройте и запустите Docker-контейнеры:

    ```bash
    docker-compose up --build
    ```

4. API будет доступен по адресу: [http://localhost:8000](http://localhost:8000).

### 2. Запуск без Docker

#### Предварительные требования

- Установленный [Python 3.9+](https://www.python.org/).
- Установленный [PostgreSQL](https://www.postgresql.org/).

#### Шаги:

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/full-est/PP2.git
    cd ваш_репозиторий
    ```

2. Установите виртуальное окружение:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # для Linux/MacOS
    venv\Scripts\activate  # для Windows
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Создайте базу данных в PostgreSQL и настройте подключение в файле `.env`:

    ```env
    DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/yourdatabase
    SECRET_KEY=your-secret-key
    ```

5. Запустите сервер:

    ```bash
    uvicorn main:app --reload
    ```

6. API будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000).

