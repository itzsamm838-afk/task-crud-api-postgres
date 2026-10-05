# A3 — Containerized FastAPI Task API

Backend AI Engineering — BE-04

This project continues the A2 Task CRUD API and replaces its SQLite storage with PostgreSQL running in Docker.

## What A3 demonstrates

- PostgreSQL running in Docker
- Persistent PostgreSQL data using a Docker named volume
- FastAPI application running in Docker
- Docker Compose starting the full stack with one command
- Database connection supplied through `.env`
- `.env.example` committed while `.env` remains gitignored
- Database schema and seed data in `schema.sql`
- PostgreSQL repository separated from the FastAPI routes
- CRUD behavior preserved from A2
- Persistence verified across app/container restarts

## Architecture

```text
FastAPI routes
      |
      v
TaskService
      |
      v
TaskRepository interface
      |
      v
PostgresTaskRepository
      |
      v
PostgreSQL container
      |
      v
Docker named volume
```

The repository layer isolates database access. The service contains task/business validation, while the routes handle HTTP behavior.

### Note about the A2 starting point

The original A2 implementation stored SQLite SQL directly inside `main.py`; it did not already contain a formal service/repository layer. For A3, the same API behavior was preserved while introducing the service/repository boundary required by the assignment. The PostgreSQL repository is therefore the storage implementation used by the service.

## Project structure

```text
.
├── main.py
├── service.py
├── repository.py
├── schema.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── screenshots/
```

Do not commit `.env`, database files, `__pycache__`, or virtual environments.

## Configuration

Copy `.env.example` to `.env` and keep the values local.

```text
POSTGRES_DB=tasks
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpassword
DATABASE_URL=postgresql://taskuser:taskpassword@db:5432/tasks
```

The app uses the Compose service name `db` as the PostgreSQL hostname.

## Run the stack

From the project directory:

```bash
docker compose up --build
```

The first startup:

1. Builds the FastAPI image.
2. Starts PostgreSQL.
3. Creates the database.
4. Runs `schema.sql`.
5. Creates the `tasks` table.
6. Inserts the seed tasks when the table is empty.
7. Starts FastAPI after PostgreSQL passes its health check.

Open:

```text
http://localhost:8000/docs
```

## Test the API

Get all tasks:

```bash
curl http://localhost:8000/tasks
```

Create a task:

```bash
curl -X POST http://localhost:8000/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Containerize the API\"}"
```

Get a task:

```bash
curl http://localhost:8000/tasks/1
```

Update a task:

```bash
curl -X PUT http://localhost:8000/tasks/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"done\":true}"
```

Delete a task:

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

Swagger UI is also available at `/docs`.

## Persistence proof

The PostgreSQL data directory is stored in the named Docker volume:

```text
postgres_data
```

To prove persistence:

1. Start the stack:

```bash
docker compose up --build
```

2. Create a new task through Swagger or curl.
3. Confirm the new task appears in `GET /tasks`.
4. Stop the containers:

```bash
docker compose down
```

5. Start them again:

```bash
docker compose up
```

6. Run `GET /tasks` again.

The created task should still exist because `docker compose down` removes the containers but does not remove the named volume.

Do **not** use:

```bash
docker compose down -v
```

for the persistence test because `-v` removes the database volume.

## Useful commands

See running containers:

```bash
docker compose ps
```

View app logs:

```bash
docker compose logs app
```

View database logs:

```bash
docker compose logs db
```

Stop the stack:

```bash
docker compose down
```

Remove the database volume only when you intentionally want a fresh database:

```bash
docker compose down -v
```

## A3 requirements checklist

- [x] PostgreSQL runs in Docker
- [x] PostgreSQL uses a persistent Docker volume
- [x] `.env` contains the connection string and is gitignored
- [x] `.env.example` is committed
- [x] `schema.sql` creates the table and seed data
- [x] PostgreSQL repository implemented
- [x] Service/repository separation introduced
- [x] CRUD API behavior preserved
- [x] FastAPI app runs in Docker
- [x] `docker compose up` starts the complete stack
- [ ] Persistence screenshot/evidence added after local verification
