import uuid

import pytest

from service.exc import UserAlreadyExistsServiceException, UserNotFoundServiceException
from service.user_service import UserService


async def create_user(user_service_: UserService, user_create_data_dict_):
    user_create_data = user_service_.to_user_create_service_model(user_create_data_dict_)
    return await user_service_.create(user_create_data)


async def test_user_create_success(user_service: UserService):
    user_create_data_dict = {
        "email": "user@example.com",
        "password": "qwerty007",
        "last_name": "ilich"
    }
    created_user = await create_user(user_service, user_create_data_dict)

    print(created_user)


async def test_user_create_already_existed(user_service: UserService):
    user_create_data_dict = {
        "email": "user@example.com",
        "password": "qwerty007",
        "last_name": "ilich"
    }
    created_user = await create_user(user_service, user_create_data_dict)

    print(created_user)

    with pytest.raises(UserAlreadyExistsServiceException):
        await create_user(user_service, user_create_data_dict)


async def test_user_update_unknown(user_service: UserService):
    user_update_data_dict = {
        "password": "12432457658756",
        "first_name": "Ivan",
        "last_name": "Ivanov"
    }
    user_update_data = user_service.to_user_update_service_model(user_update_data_dict)

    with pytest.raises(UserNotFoundServiceException):
        updated_user = await user_service.update(uuid.uuid4(), user_update_data)
        print(updated_user)


async def test_user_update_success(user_service: UserService):
    user_create_data_dict = {
        "email": "user@example.com",
        "password": "qwerty007",
        "last_name": "ilich"
    }
    created_user = await create_user(user_service, user_create_data_dict)

    user_update_data_dict = {
        "password": "12432457658756",
        "first_name": "Ivan",
        "last_name": "Ivanov"
    }
    user_update_data = user_service.to_user_update_service_model(user_update_data_dict)

    updated_user = await user_service.update(created_user.id, user_update_data)
    print(updated_user)

    user_update_data_dict = {}
    user_update_data = user_service.to_user_update_service_model(user_update_data_dict)

    updated_user = await user_service.update(created_user.id, user_update_data)
    print(updated_user)


async def test_user_delete_unknown(user_service: UserService):
    with pytest.raises(UserNotFoundServiceException):
        await user_service.delete(uuid.uuid4())


async def test_user_delete_success(user_service: UserService):
    user_create_data_dict = {
        "email": "user@example.com",
        "password": "qwerty007",
        "last_name": "ilich"
    }
    created_user = await create_user(user_service, user_create_data_dict)

    await user_service.delete(created_user.id)


async def test_user_get_by_id_unknown(user_service: UserService):
    with pytest.raises(UserNotFoundServiceException):
        await user_service.get_by_id(uuid.uuid4())


async def test_user_get_by_id_success(user_service: UserService):
    user_create_data_dict = {
        "email": "user@example.com",
        "password": "qwerty007",
        "last_name": "ilich"
    }
    created_user = await create_user(user_service, user_create_data_dict)

    selected_user = await user_service.get_by_id(created_user.id)
    print(selected_user)
