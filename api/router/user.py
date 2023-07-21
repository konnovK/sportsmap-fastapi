import uuid

from fastapi import APIRouter, HTTPException, Depends

from api.dependencies import jwt_authenticate_user, get_app_context
from api.context import AppContext
from api.schema.user import (
    UserCreateRequest,
    UserLoginResponse,
    UserPatchRequest,
    UserResponse
)

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('', status_code=201)
async def create_user(
        body: UserCreateRequest,
        app_context: AppContext = Depends(get_app_context)
) -> UserLoginResponse:
    raise HTTPException(501)


@router.patch('/{id}')
async def patch_user(
        id: uuid.UUID,
        body: UserPatchRequest,
        authenticated_user_id=Depends(jwt_authenticate_user),
        app_context: AppContext = Depends(get_app_context)
) -> UserResponse:
    raise HTTPException(501)


@router.delete('/{id}', status_code=204)
async def delete_user(
        id: uuid.UUID,
        authenticated_user_id=Depends(jwt_authenticate_user),
        app_context: AppContext = Depends(get_app_context)
):
    raise HTTPException(501)


@router.get('/{id}')
async def get_user_by_id(id: uuid.UUID):
    raise HTTPException(501)


@router.post('/login')
async def login():
    raise HTTPException(501)


@router.post('/token/refresh')
async def refresh_token(authenticated_user_id=Depends(jwt_authenticate_user)):
    raise HTTPException(501)


@router.post('/password-refresh/{secret}')
async def refresh_password():
    raise HTTPException(501)
