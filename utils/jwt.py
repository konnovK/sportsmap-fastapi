import time
from typing import Tuple
import jwt
from loguru import logger

JWT_SECRET = 'ehjkpearhjgoikgsvbuiesgftewuyvgBL'
JWT_TTL_SECONDS = 15 * 60


class JWTException(Exception):
    pass


class AuthorizationException(Exception):
    pass


def _encode_jwt(data: dict) -> str:
    logger.trace(f'ENCODE JWT FOR {data}')
    try:
        return jwt.encode(data, JWT_SECRET, algorithm="HS256")
    except Exception:
        raise JWTException


def _decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise JWTException


def create_jwt(id: str) -> Tuple[str, str, int]:
    """
    Создает access token и refresh token, принимает `id` пользователя.

    Возвращает тройку (access_token, refresh_token, expires_in).

    Выбрасывает JWTException, если случилась ошибка при создании токенов.
    """
    now = int(time.time())
    expires_in = JWT_TTL_SECONDS

    access_token = _encode_jwt({
        'id': id,
        'iat': now,
        'expires_in': expires_in,
        'end_at': now + expires_in
    })
    refresh_token = _encode_jwt({
        'id': id,
        'iat': now,
        'access_token': access_token
    })
    return access_token, refresh_token, expires_in


def check_access_token_unexpired(access_token: str) -> bool:
    return True


def get_id_from_access_token(access_token: str) -> str:
    access_token_data = _decode_jwt(access_token)
    try:
        access_token_id = access_token_data['id']
    except ValueError:
        raise JWTException
    return access_token_id
