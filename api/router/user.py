import uuid

from fastapi import APIRouter, HTTPException, Depends

from api.dependencies import jwt_authenticate_user, get_app_context
from api.context import AppContext
from api.schema.user import (
    UserCreateRequest,
    UserLoginResponse,
    UserPatchRequest,
    UserResponse,
    UserLoginRequest,
    UserRefreshTokenRequest, UserRefreshPassword
)
from api.utils.jwt import create_jwt, get_id_from_access_token, JWTException, check_refresh_token_correct
from service.exc import UserNotFoundServiceException

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('', status_code=201)
async def create_user(
        body: UserCreateRequest,
        app_context: AppContext = Depends(get_app_context)
) -> UserLoginResponse:
    created_user = await app_context.user_service.create(body)
    access_token, refresh_token, expires_in = create_jwt(str(created_user.id))
    return UserLoginResponse(
        **created_user.model_dump(),
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expires_in=expires_in
    )


@router.patch('/{id}')
async def patch_user(
        id: uuid.UUID,
        body: UserPatchRequest,
        authenticated_user_id: str = Depends(jwt_authenticate_user),
        app_context: AppContext = Depends(get_app_context)
) -> UserResponse:
    if await app_context.user_service.check_is_admin_by_id(authenticated_user_id):
        updated_user = await app_context.user_service.update(id, body)
        return updated_user
    else:
        if str(id) == authenticated_user_id:
            updated_user = await app_context.user_service.update(id, body)
            return updated_user
        else:
            raise HTTPException(403, {"message": "У вас недостаточно прав для обновления данных об этом пользователе."})


@router.delete('/{id}', status_code=204)
async def delete_user(
        id: uuid.UUID,
        authenticated_user_id: str = Depends(jwt_authenticate_user),
        app_context: AppContext = Depends(get_app_context)
):
    if await app_context.user_service.check_is_admin_by_id(authenticated_user_id):
        if str(id) == authenticated_user_id:
            raise HTTPException(403, {"message": "У вас недостаточно прав для удаления этого пользователя."})
        else:
            await app_context.user_service.delete(id)
    else:
        if str(id) == authenticated_user_id:
            await app_context.user_service.delete(id)
        else:
            raise HTTPException(403, {"message": "У вас недостаточно прав для удаления этого пользователя."})
    raise HTTPException(501)


@router.get('/{id}')
async def get_user_by_id(
        id: uuid.UUID,
        app_context: AppContext = Depends(get_app_context)
):
    selected_user = await app_context.user_service.get_by_id(id)
    return selected_user


@router.post('/login')
async def login(
        body: UserLoginRequest,
        app_context: AppContext = Depends(get_app_context)
):
    selected_user = await app_context.user_service.get_by_email_and_password(body.email, body.password)
    access_token, refresh_token, expires_in = create_jwt(str(selected_user.id))
    return UserLoginResponse(
        **selected_user.model_dump(),
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expires_in=expires_in
    )


@router.post('/token/refresh')
async def refresh_token(
        body: UserRefreshTokenRequest,
        app_context: AppContext = Depends(get_app_context)
) -> UserLoginResponse:
    try:
        if not check_refresh_token_correct(body.access_token, body.refresh_token):
            raise HTTPException(400, {"message": "Некорректный токен"})
        user_id = get_id_from_access_token(body.access_token)
        existed_user = await app_context.user_service.get_by_id(user_id)
    except JWTException or UserNotFoundServiceException:
        raise HTTPException(400, {"message": "Некорректный токен"})
    access_token, refresh_token, expires_in = create_jwt(user_id)
    return UserLoginResponse(
        **existed_user.model_dump(),
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expires_in=expires_in
    )


@router.post('/password-refresh/{secret}')
async def refresh_password(
    secret: str,
    body: UserRefreshPassword,
    app_context: AppContext = Depends(get_app_context)
):
    user_password_refresh = await app_context.email_service.get_by_secret_email_password_refresh(secret)
    email = user_password_refresh.email
    await app_context.user_service.update_password_by_email(email, body.new_password)
    await app_context.email_service.delete_by_email_email_password_refresh(email)
