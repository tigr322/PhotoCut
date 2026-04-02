from fastapi import APIRouter

from app.api.v1.endpoints import api_keys, auth, files, jobs, me

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(me.router, tags=["users"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
