import hashlib

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.model.user import User

from service.utils import USER_PK_TYPE, SALT
from service.exc import UserAlreadyExistsServiceException, UserNotFoundServiceException
from service.model.user_model import (
    UserCreateServiceModel,
    UserServiceModel,
    UserUpdateServiceModel
)


class UserService:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    @staticmethod
    def _hash_password(email: str, password: str) -> str:
        return hashlib.sha256((password + email + SALT).encode()).hexdigest()

    @staticmethod
    def to_user_create_service_model(user_data: dict):
        return UserCreateServiceModel.model_validate(user_data)

    @staticmethod
    def to_user_update_service_model(user_date: dict):
        return UserUpdateServiceModel.model_validate(user_date)

    async def create(self, user_create_data: UserCreateServiceModel) -> UserServiceModel:
        """
        :raise UserAlreadyExistsServiceException:
        :param user_create_data:
        :return:
        """
        password_hash = UserService._hash_password(user_create_data.email, user_create_data.password)

        user_data_as_dict = user_create_data.model_dump()
        user_data_as_dict.pop("password")
        user_data_as_dict["password_hash"] = password_hash

        async with self.async_session() as session:
            session: AsyncSession
            created_user = User(**user_data_as_dict)
            try:
                session.add(created_user)
                await session.commit()
                await session.refresh(created_user)
            except IntegrityError:
                raise UserAlreadyExistsServiceException
        return UserServiceModel.model_validate(created_user)

    async def update(self, pk: USER_PK_TYPE, user_update_data: UserUpdateServiceModel) -> UserServiceModel:
        """
        Меняет некоторые поля юзера по его id.
        :raise UserNotFoundServiceException:
        :param pk:
        :param user_update_data:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            selected_user: User = (await session.execute(sa.select(User).where(User.id == pk))).scalar()
            if selected_user is None:
                raise UserNotFoundServiceException

            if user_update_data.password is not None:
                new_password_hash = UserService._hash_password(selected_user.email, user_update_data.password)
                selected_user.password_hash = new_password_hash

            if user_update_data.first_name is not None:
                selected_user.first_name = user_update_data.first_name

            if user_update_data.last_name is not None:
                selected_user.last_name = user_update_data.last_name

            await session.commit()
            await session.refresh(selected_user)

            return UserServiceModel.model_validate(selected_user)

    async def delete(self, pk: USER_PK_TYPE):
        """
        :raise UserNotFoundServiceException:
        :param pk:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            selected_user: User = (await session.execute(sa.select(User).where(User.id == pk))).scalar()
            if selected_user is None:
                raise UserNotFoundServiceException
            await session.delete(selected_user)
            await session.commit()

    async def get_by_id(self, pk: USER_PK_TYPE) -> UserServiceModel:
        """
        :raise UserNotFoundServiceException:
        :param pk:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            selected_user: User = (await session.execute(sa.select(User).where(User.id == pk))).scalar()
            if selected_user is None:
                raise UserNotFoundServiceException
            return UserServiceModel.model_validate(selected_user)

    async def check_exists_by_id(self, pk: USER_PK_TYPE) -> bool:
        async with self.async_session() as session:
            session: AsyncSession
            selected_user_id = (await session.execute(sa.select(User.id).where(User.id == pk))).scalar()
            return selected_user_id is not None

    async def check_exists_by_email(self, email: str) -> bool:
        async with self.async_session() as session:
            session: AsyncSession
            selected_user_id = (await session.execute(sa.select(User.id).where(User.email == email))).scalar()
            return selected_user_id is not None

    async def check_is_admin_by_id(self, pk: USER_PK_TYPE) -> bool:
        """
        :raise UserNotFoundServiceException:
        :param pk:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            is_admin = (await session.execute(sa.select(User.admin).where(User.id == pk))).scalar()
            if is_admin is None:
                raise UserNotFoundServiceException
            return is_admin
