# AGENTS.md

## Cursor Cloud specific instructions

Bobyard Comments is a two-service full-stack app: a FastAPI + SQLite backend and a React (Vite) frontend. See `README.md` for the product/API overview and `comments-app/README.md` for frontend template notes.

### Services

- Backend (`backend/`): FastAPI (Python 3.12), SQLAlchemy, SQLite. On startup it creates tables and seeds from `backend/data/comments.json` if the DB is empty. Dependencies live in a local virtualenv at `backend/.venv` (created by the update script).
- Frontend (`comments-app/`): React 19 + Vite 8. Uses `npm` (there is a `package-lock.json`). The API base URL is hard-coded to `http://localhost:8000/api/comments` in `comments-app/src/api/comments.js`.

### Running (dev mode)

- Backend: `cd backend && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
  - Health: `http://localhost:8000/health`, docs: `http://localhost:8000/docs`.
  - Default DB is a SQLite file `backend/comments.db` (created on first run). Override with `DATABASE_URL`.
- Frontend: `cd comments-app && npm run dev` — serves on `http://localhost:5173` (Vite default), NOT the `5174` port used by the Docker/nginx production setup. The backend CORS list already allows `5173`, `5174`, `3000`, and `8080`.
- Both dev servers must run at the same time for the UI to load comments (frontend calls the backend directly on port 8000).

### Lint / test / build

- Frontend lint: `cd comments-app && npm run lint` (ESLint).
- Frontend build: `cd comments-app && npm run build` (`tsc -b && vite build`).
- There is no automated test suite in this repo.

### Gotchas

- Do not rely on Docker for dev iteration here; `docker compose up` builds production images (nginx-served frontend on `5174`). For development use the `uvicorn --reload` + `npm run dev` commands above.
- `backend/requirements.txt` includes `psycopg[binary]` (Postgres driver) but the app runs on SQLite by default; no Postgres server is needed.
