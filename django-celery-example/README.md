# Django + Celery Docker Example

A minimal example of **async image generation** with Django, Celery, Redis, and PostgreSQL — the pattern you'd use to avoid HTTP timeouts for long-running tasks.

## Architecture

```text
Client
  │
  ▼
Django (web) ── POST /api/jobs/ ──► returns 202 + job_id immediately
  │                                      │
  │                                      ▼
  │                                 Redis (broker)
  │                                      │
  │                                      ▼
  │                              Celery Worker
  │                              (slow image gen)
  │                                      │
  ▼                                      ▼
PostgreSQL ◄──── job status / order_index ────► media volume (PNG files)
```

## Services

| Service | Role |
|---------|------|
| `web` | Django + Gunicorn API |
| `celery_worker` | Runs `generate_image` tasks |
| `celery_beat` | Celery scheduler (included for completeness) |
| `redis` | Message broker + result backend |
| `postgres` | Job metadata (status, progress, order) |

## Quick start

```bash
cd django-celery-example
docker compose up --build
```

API: http://localhost:8001/api/jobs/

## Try it

### 1. Create a generation job (returns immediately, no HTTP timeout)

```bash
curl -X POST http://localhost:8001/api/jobs/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cat riding a skateboard"}'
```

Response (`202 Accepted`):

```json
{
  "id": 1,
  "prompt": "a cat riding a skateboard",
  "order_index": 1,
  "status": "pending",
  "progress": 0,
  "celery_task_id": "...",
  "result_url": null,
  ...
}
```

### 2. Poll job status

```bash
curl http://localhost:8001/api/jobs/1/
```

Watch `status` go `pending → processing → completed` and `progress` increase.

### 3. List jobs (sorted by `order_index`)

```bash
curl http://localhost:8001/api/jobs/
```

Submit multiple jobs quickly — they may **finish out of order**, but the list is always sorted by `order_index`.

## Key code paths

| File | What it does |
|------|--------------|
| `jobs/views.py` | `POST` creates DB record + `generate_image.delay()` |
| `jobs/tasks.py` | Celery task simulates slow generation, updates progress |
| `jobs/models.py` | `GenerationJob` with `order_index`, `status`, `progress` |
| `config/celery.py` | Celery app bootstrap |
| `docker-compose.yml` | Separate containers for web / worker / beat |

## How this maps to interview answers

- **HTTP timeout** → API returns `202` immediately; worker runs async
- **Long generation** → Celery worker sleeps + updates `progress` in DB
- **Ordering** → `order_index` assigned at creation; display sorted regardless of completion order
- **Retries** → `@shared_task(autoretry_for=..., max_retries=3)`

## Local dev (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start Postgres + Redis yourself, then:
export DJANGO_SETTINGS_MODULE=config.settings
export POSTGRES_HOST=localhost
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/1

python manage.py migrate
python manage.py runserver

# In another terminal:
celery -A config worker --loglevel=info
```

## Stop

```bash
docker compose down
docker compose down -v   # also delete DB + media volumes
```
