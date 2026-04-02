# PhotoCut MVP

A production-minded MVP for background removal and photo processing as a web SaaS + open REST API.

## Stack

### Backend
- Python 3.12
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Redis
- RQ worker
- rembg
- Pillow

### Frontend
- Nuxt 3
- Vue 3
- TypeScript
- Tailwind CSS
- Pinia

### Infra
- Docker
- Docker Compose

## Architecture

```text
.
├── backend
│   ├── app
│   │   ├── api
│   │   │   ├── deps.py
│   │   │   └── v1
│   │   │       ├── endpoints
│   │   │       │   ├── api_keys.py
│   │   │       │   ├── auth.py
│   │   │       │   ├── files.py
│   │   │       │   ├── jobs.py
│   │   │       │   └── me.py
│   │   │       └── router.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   ├── redis.py
│   │   │   └── security.py
│   │   ├── db
│   │   │   ├── base.py
│   │   │   ├── base_class.py
│   │   │   └── session.py
│   │   ├── models
│   │   │   ├── api_key.py
│   │   │   ├── file.py
│   │   │   ├── job.py
│   │   │   └── user.py
│   │   ├── schemas
│   │   │   ├── api_key.py
│   │   │   ├── auth.py
│   │   │   ├── file.py
│   │   │   ├── job.py
│   │   │   └── user.py
│   │   ├── services
│   │   │   ├── api_key_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── file_service.py
│   │   │   ├── image_processing_service.py
│   │   │   ├── job_service.py
│   │   │   └── storage.py
│   │   ├── workers
│   │   │   ├── tasks.py
│   │   │   └── worker.py
│   │   └── main.py
│   ├── alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── 20260402_0001_initial.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── assets/css/tailwind.css
│   ├── components
│   │   ├── JobStatusBadge.vue
│   │   ├── ToastStack.vue
│   │   └── UploadDropzone.vue
│   ├── composables
│   │   ├── useApi.ts
│   │   └── useToast.ts
│   ├── middleware
│   │   ├── auth.ts
│   │   └── guest.ts
│   ├── pages
│   │   ├── api-keys.vue
│   │   ├── dashboard.vue
│   │   ├── index.vue
│   │   ├── jobs.vue
│   │   ├── login.vue
│   │   └── register.vue
│   ├── stores/auth.ts
│   ├── types/index.ts
│   ├── Dockerfile
│   ├── nuxt.config.ts
│   └── package.json
├── docker-compose.yml
└── .env.example
```

## Implemented Features

- User registration/login with JWT authentication
- `/api/v1/me` profile endpoint
- API key management (create/list/revoke)
  - Raw key shown only once
  - Only hashed key + prefix stored in DB
- Async image job pipeline via Redis + RQ
- Job statuses: `pending`, `queued`, `processing`, `completed`, `failed`
- Image processing:
  - background removal (`rembg`)
  - transparent PNG output
  - optional resize
  - optional crop
  - optional fit-to-canvas
  - optional format conversion (`png`, `jpeg`, `webp`)
  - metadata stripping via re-encode
- Local storage abstraction (`StorageInterface` + `LocalStorageService`)
- Authenticated file download endpoint
- Nuxt dashboard with:
  - drag/drop upload
  - job polling/status
  - download links
  - API key management UI

## API Endpoints

### Auth
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/me`

### API Keys
- `GET /api/v1/api-keys`
- `POST /api/v1/api-keys`
- `DELETE /api/v1/api-keys/{id}`

### Jobs + Files
- `POST /api/v1/jobs/remove-background`
- `GET /api/v1/jobs`
- `GET /api/v1/jobs/{job_id}`
- `GET /api/v1/files/{file_id}`

### Health
- `GET /health`
- `GET /ready`

OpenAPI docs:
- [http://localhost:8000/docs](http://localhost:8000/docs)

## Run With Docker Compose

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Start all services:

```bash
docker compose up --build
```

3. Open:
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Notes

- Backend and worker share `./backend/data` for local file storage.
- Migrations are applied automatically when backend starts.
- API supports both `Authorization: Bearer <jwt>` and `X-API-Key: <raw_key>` for job/file endpoints.

## Future Extension Ready

This MVP is intentionally small but prepared for:
- S3/MinIO storage by implementing another `StorageInterface`
- billing/quotas/webhooks via additional tables + service layer
- batch jobs and extra image operations by extending job options and worker tasks
