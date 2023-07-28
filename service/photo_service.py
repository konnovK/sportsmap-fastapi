import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.model.facility import FacilityPhoto, Facility
from service.exc import FacilityNotFoundServiceException, PhotoNotFoundServiceException
from service.model.photo_model import PhotoServiceModel


class PhotoService:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    async def create(self, url: str, filename: str, facility_id) -> PhotoServiceModel:
        async with self.async_session() as session:
            session: AsyncSession

            photo = await FacilityPhoto.get_or_create(session, url, filename)

            facility: Facility = (await session.execute(sa.select(Facility).where(Facility.id == facility_id))).scalar()
            if facility is None:
                raise FacilityNotFoundServiceException('Такого спортивного объекта не существует.')

            facility.photo.append(photo)

            await session.commit()
            await session.refresh(photo)
        return PhotoServiceModel.model_validate(photo)

    async def delete(self, facility_id, photo_id) -> str:
        """
        Удаляет фото из бд и возвращает его filename.
        :param facility_id:
        :param photo_id:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession

            facility: Facility = (await session.execute(sa.select(Facility).where(Facility.id == facility_id))).scalar()
            if facility is None:
                raise FacilityNotFoundServiceException('Такого спортивного объекта не существует.')

            photo: FacilityPhoto = await FacilityPhoto.get_by_id(session, photo_id)
            if photo is None:
                raise PhotoNotFoundServiceException('Такой фотографии не существует.')

            filename = photo.filename

            if photo not in facility.photo:
                raise PhotoNotFoundServiceException('Такой фотографии нет у данного спортивного объекта.')

            facility.photo.remove(photo)
            await session.commit()
        return filename
