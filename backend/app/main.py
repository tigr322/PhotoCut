from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.redis import get_redis_connection
from app.db.session import SessionLocal

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    db = None
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database not ready") from exc
    finally:
        if db is not None:
            db.close()

    try:
        get_redis_connection().ping()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Redis not ready") from exc

    return {"status": "ready"}
