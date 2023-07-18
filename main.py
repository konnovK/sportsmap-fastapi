import asyncio

from db.db import DB
from service.model.user_model import UserCreateServiceModel, UserUpdateServiceModel
from service.user_service import UserService
from settings import Settings


async def main():
    settings = Settings.new()
    db = DB(settings=settings)
    user_service = UserService(async_session=db.async_session)

    create_user_data = UserCreateServiceModel.model_validate({
        "email": "user1@example.com",
        "password": "1234"
    })
    update_user_data = UserUpdateServiceModel.model_validate({
        "first_name": "boris",
        "password": "qwerty"
    })

    created_user = await user_service.create(create_user_data)

    updated_user = await user_service.update(created_user.id, update_user_data)

    print(updated_user)


if __name__ == '__main__':
    asyncio.run(main())