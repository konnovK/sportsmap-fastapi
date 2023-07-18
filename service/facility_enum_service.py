from typing import TypeAlias

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.model.facility import FacilityType, FacilityOwningType, FacilityCoveringType, FacilityPayingType, FacilityAge
from service.model.facility_model import FacilityTypeServiceModel


class FacilityEnumService:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    @staticmethod
    def service_model_to_str(ft: FacilityTypeServiceModel) -> str:
        return ft.name

    async def _get_all_facility_enum_by_cls(self, cls: TypeAlias) -> list[FacilityTypeServiceModel]:
        async with self.async_session() as session:
            session: AsyncSession
            fts = (await session.execute(sa.select(cls))).scalars().all()
            return [FacilityTypeServiceModel.model_validate(ft) for ft in fts]

    async def get_all_facility_types(self) -> list[FacilityTypeServiceModel]:
        return await self._get_all_facility_enum_by_cls(FacilityType)

    async def get_all_facility_owning_types(self) -> list[FacilityTypeServiceModel]:
        return await self._get_all_facility_enum_by_cls(FacilityOwningType)

    async def get_all_facility_covering_types(self) -> list[FacilityTypeServiceModel]:
        return await self._get_all_facility_enum_by_cls(FacilityCoveringType)

    async def get_all_facility_paying_types(self) -> list[FacilityTypeServiceModel]:
        return await self._get_all_facility_enum_by_cls(FacilityPayingType)

    async def get_all_facility_ages(self) -> list[FacilityTypeServiceModel]:
        return await self._get_all_facility_enum_by_cls(FacilityAge)
