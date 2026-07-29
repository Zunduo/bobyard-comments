# Bobyard Comments

Full-stack comment CRUD app (list / add / edit / delete), similar to a simple YouTube-style comment section.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Database | SQLite |
| Frontend | React (Vite) |
| Deploy | Docker Compose (backend + nginx frontend) |

## Project layout

```text
bobyard-comments/
├── backend/
│   ├── app/              # FastAPI app (routes, models, CRUD, schemas)
│   ├── data/comments.json
│   ├── Dockerfile
│   └── requirements.txt
├── comments-app/         # React frontend
│   ├── src/
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## API

| Method | Path | Body |
|--------|------|------|
| `GET` | `/api/comments` | — |
| `POST` | `/api/comments` | `{ "text": "..." }` → author `Admin`, date=now, likes=`0` |
| `PATCH` | `/api/comments/{id}` | `{ "text": "..." }` |
| `DELETE` | `/api/comments/{id}` | — (204 No Content) |

Interactive docs: http://localhost:8000/docs

## Quick start (Docker)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5174 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |

SQLite is stored in the Docker volume `comments_sqlite`.

```bash
docker compose down        # stop
docker compose down -v     # stop and delete DB volume
```