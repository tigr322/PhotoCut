import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.api_key import ApiKeyCreateRequest, ApiKeyCreateResponse, ApiKeyOut
from app.services.api_key_service import ApiKeyService

router = APIRouter()


@router.get("", response_model=list[ApiKeyOut])
def list_api_keys(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ApiKeyOut]:
    keys = ApiKeyService(db).list_keys(user_id=current_user.id)
    return [ApiKeyOut.model_validate(key) for key in keys]


@router.post("", response_model=ApiKeyCreateResponse, status_code=status.HTTP_201_CREATED)
def create_api_key(
    payload: ApiKeyCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApiKeyCreateResponse:
    api_key, raw_key = ApiKeyService(db).create_key(user_id=current_user.id, name=payload.name)
    return ApiKeyCreateResponse(
        id=api_key.id,
        name=api_key.name,
        key_prefix=api_key.key_prefix,
        key=raw_key,
        created_at=api_key.created_at,
    )


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    key_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    ApiKeyService(db).revoke_key(user_id=current_user.id, key_id=key_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
