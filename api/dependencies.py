from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from api.context import AppContext
from utils.jwt import check_access_token_unexpired, get_id_from_access_token

from api.globals import app_context

security = HTTPBearer()


async def jwt_authenticate_user(authorization=Depends(security)) -> str:
    if authorization is None:
        raise HTTPException(401, 'no access token')
    scheme = authorization.scheme
    token = authorization.credentials

    if scheme != 'Bearer':
        raise HTTPException(401, 'wrong access token scheme')
    if token is None:
        raise HTTPException(401, 'no access token')
    try:
        unexpired = check_access_token_unexpired(token)
    except Exception:
        raise HTTPException(401, 'wrong access token format')
    if not unexpired:
        raise HTTPException(401, 'expired access token')
    try:
        user_id = get_id_from_access_token(token)
    except Exception:
        raise HTTPException(401, 'wrong access token')
    if not (await app_context.user_controller.exists(user_id)):
        raise HTTPException(401, 'wrong access token')
    return user_id


async def get_app_context() -> AppContext:
    return app_context
