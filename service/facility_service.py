from typing import Any

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.model.facility import Facility, FacilityPayingType, FacilityAge, FacilityType, FacilityOwningType, \
    FacilityCoveringType
from service.utils import FACILITY_PK_TYPE
from service.exc import FacilityAlreadyExistsServiceException, FacilityNotFoundServiceException
from service.model.facility_model import (
    FacilityServiceModel,
    FacilityCreateServiceModel,
    FacilityPutServiceModel,
    FacilityPatchServiceModel
)


class FacilityService:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session

    @staticmethod
    def to_facility_create_service_model(facility_data: dict):
        return FacilityCreateServiceModel.model_validate(facility_data)

    @staticmethod
    def to_facility_patch_service_model(facility_data: dict):
        return FacilityPatchServiceModel.model_validate(facility_data)

    @staticmethod
    def to_facility_put_service_model(facility_data: dict):
        return FacilityPutServiceModel.model_validate(facility_data)

    @staticmethod
    async def _transform_facility_data(facility_data: dict, session: AsyncSession) -> dict:
        facility_data_type_name = facility_data.pop("type")
        facility_data["type"] = await FacilityType.get_or_create(session, facility_data_type_name)

        facility_data_owning_type = facility_data.pop("owning_type")
        facility_data["owning_type"] = await FacilityOwningType.get_or_create(session, facility_data_owning_type)

        facility_data_covering_type = facility_data.pop("covering_type")
        if facility_data_covering_type is not None:
            facility_data["covering_type"] = await FacilityCoveringType.get_or_create(
                session, facility_data_covering_type
            )

        facility_data_paying_type: list[str] = facility_data.pop("paying_type")
        paying_types = []
        for fpt in facility_data_paying_type:
            pt = await FacilityPayingType.get_or_create(session, fpt)
            paying_types.append(pt)
        facility_data["paying_type"] = paying_types

        facility_data_ages: list[str] = facility_data.pop("age")
        ages = []
        for fa in facility_data_ages:
            a = await FacilityAge.get_or_create(session, fa)
            ages.append(a)
        facility_data["age"] = ages
        return facility_data

    async def create(self, facility_create_data: FacilityCreateServiceModel) -> FacilityServiceModel:
        """
        :raise FacilityAlreadyExistsServiceException:
        :param facility_create_data:
        :return:
        """
        facility_data = facility_create_data.model_dump()

        async with self.async_session() as session:
            session: AsyncSession

            facility_data = await FacilityService._transform_facility_data(facility_data, session)

            created_facility = Facility(**facility_data)

            try:
                session.add(created_facility)
                await session.commit()
                await session.refresh(created_facility)
            except IntegrityError:
                raise FacilityAlreadyExistsServiceException("Такой спортивный объект уже существует.")
        return FacilityServiceModel.model_validate(created_facility)

    async def put(self, pk: FACILITY_PK_TYPE, facility_put_data: FacilityPutServiceModel) -> FacilityServiceModel:
        """
        :raise FacilityNotFoundServiceException:
        :param pk:
        :param facility_put_data:
        :return:
        """
        facility_data = facility_put_data.model_dump()

        async with self.async_session() as session:
            session: AsyncSession
            selected_facility: Facility = (await session.execute(sa.select(Facility).where(Facility.id == pk))).scalar()
            if selected_facility is None:
                raise FacilityNotFoundServiceException("Такого спортивного объекта не существует.")

            facility_data = await FacilityService._transform_facility_data(facility_data, session)

            for k, v in facility_data.items():
                setattr(selected_facility, k, v)

            try:
                await session.commit()
                await session.refresh(selected_facility)
            except IntegrityError:
                raise FacilityAlreadyExistsServiceException("Такой спортивный объект уже существует.")
        return FacilityServiceModel.model_validate(selected_facility)

    async def patch(self, pk: FACILITY_PK_TYPE, facility_patch_data: FacilityPatchServiceModel) -> FacilityServiceModel:
        """
        :raise FacilityNotFoundServiceException:
        :param pk:
        :param facility_patch_data:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            selected_facility: Facility = (await session.execute(sa.select(Facility).where(Facility.id == pk))).scalar()
            if selected_facility is None:
                raise FacilityNotFoundServiceException("Такого спортивного объекта не существует.")
            for k in facility_patch_data.model_fields_set:
                v = getattr(facility_patch_data, k)
                v: Any
                if k == 'type':
                    v = await FacilityType.get_or_create(session, v)
                if k == 'owning_type':
                    v = await FacilityOwningType.get_or_create(session, v)
                if k == 'covering_type':
                    v = await FacilityCoveringType.get_or_create(session, v)
                if k == 'paying_type':
                    v: list[str]
                    pts = []
                    for pt in v:
                        ppt = await FacilityPayingType.get_or_create(session, pt)
                        pts.append(ppt)
                    v = pts
                if k == "age":
                    v: list[str]
                    pts = []
                    for pt in v:
                        ppt = await FacilityAge.get_or_create(session, pt)
                        pts.append(ppt)
                    v = pts
                setattr(selected_facility, k, v)
            try:
                await session.commit()
                await session.refresh(selected_facility)
            except IntegrityError:
                raise FacilityAlreadyExistsServiceException("Такой спортивный объект уже существует.")
        return FacilityServiceModel.model_validate(selected_facility)

    async def delete(self, pk: FACILITY_PK_TYPE):
        """
        :raise FacilityNotFoundServiceException:
        :param pk:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            selected_facility = (await session.execute(sa.select(Facility).where(Facility.id == pk))).scalar()
            if selected_facility is None:
                raise FacilityNotFoundServiceException("Такого спортивного объекта не существует.")
            await session.delete(selected_facility)
            await session.commit()

    async def get_by_id(self, pk: FACILITY_PK_TYPE) -> FacilityServiceModel:
        """
        :raise FacilityNotFoundServiceException:
        :param pk:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            selected_facility = (await session.execute(sa.select(Facility).where(Facility.id == pk))).scalar()
            if selected_facility is None:
                raise FacilityNotFoundServiceException("Такого спортивного объекта не существует.")
        return FacilityServiceModel.model_validate(selected_facility)

    async def search(
            self,
            all: bool,
            q: str,
            limit: int,
            offset: int,
            order_by: str,
            order_desc: bool,

            hidden: bool,

            type: list[str],
            owning_type: list[str],
            covering_type: list[str],
            paying_type: list[str],
            age: list[str],

            filters: list[dict],
            x: float | None = None,
            y: float | None = None
    ) -> (int, list[FacilityServiceModel]):
        stmt = sa.select(Facility)
        stmt_count = sa.select(sa.func.count()).select_from(Facility)

        epsilon = 1 / 1000

        if x is not None and y is not None:
            stmt = stmt \
                .where(Facility.x >= x - epsilon).where(Facility.x <= x + epsilon) \
                .where(Facility.y >= y - epsilon).where(Facility.y <= y + epsilon)
            stmt_count = stmt_count \
                .where(Facility.x >= x - epsilon).where(Facility.x <= x + epsilon) \
                .where(Facility.y >= y - epsilon).where(Facility.y <= y + epsilon)

        if q is not None:
            stmt = stmt.where(sa.or_(
                Facility.name.icontains(q, autoescape=True),
                Facility.address.icontains(q, autoescape=True),
                Facility.owner.icontains(q, autoescape=True),
                Facility.type_name.icontains(q, autoescape=True),
            ))
            stmt_count = stmt_count.where(sa.or_(
                Facility.name.icontains(q, autoescape=True),
                Facility.address.icontains(q, autoescape=True),
                Facility.owner.icontains(q, autoescape=True),
                Facility.type_name.icontains(q, autoescape=True),
            ))

        if hidden is not None:
            stmt = stmt.where(Facility.hidden == hidden)
            stmt_count = stmt_count.where(Facility.hidden == hidden)

        if type is not None and len(type) > 0:
            stmt = stmt.where(Facility.type_name.in_(type))
            stmt_count = stmt_count.where(Facility.type_name.in_(type))
        if owning_type is not None and len(owning_type) > 0:
            stmt = stmt.where(Facility.owning_type_name.in_(owning_type))
            stmt_count = stmt_count.where(Facility.owning_type_name.in_(owning_type))
        if covering_type is not None and len(covering_type) > 0:
            stmt = stmt.where(Facility.covering_type_name.in_(covering_type))
            stmt_count = stmt_count.where(Facility.covering_type_name.in_(covering_type))

        if paying_type:
            if len(paying_type) > 0:
                stmt = stmt.where(Facility.paying_type.any(FacilityPayingType.name.in_(paying_type)))
                stmt_count = stmt_count.where(Facility.paying_type.any(FacilityPayingType.name.in_(paying_type)))

        if age:
            if len(age) > 0:
                stmt = stmt.where(Facility.age.any(FacilityAge.name.in_(age)))
                stmt_count = stmt_count.where(Facility.age.any(FacilityAge.name.in_(age)))

        if filters is not None:
            for f in filters:
                field = f['field']
                eq = f.get('eq')
                lt = f.get('lt')
                gt = f.get('gt')
                conditions = []
                if eq is not None:
                    conditions.append(getattr(Facility, field) == eq)
                if lt is not None:
                    conditions.append(getattr(Facility, field) <= lt)
                if gt is not None:
                    conditions.append(getattr(Facility, field) >= gt)
                stmt = stmt.where(sa.and_(*conditions))
                stmt_count = stmt_count.where(sa.and_(*conditions))

        if order_by in ['created_at', 'type', 'area', 'actual_workload', 'eps', 'annual_capacity']:
            if order_by == 'type':
                order_by = f"{order_by}_name"
        else:
            order_by = "name"
        if order_desc is not None and order_desc is True:
            stmt = stmt.order_by(sa.desc(order_by))
        else:
            stmt = stmt.order_by(order_by)

        if not all:
            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)

        async with self.async_session() as session:
            session: AsyncSession
            facilities = (await session.execute(stmt)).scalars().all()
            count = (await session.execute(stmt_count)).scalar()

        return count, [FacilityServiceModel.model_validate(f) for f in facilities]
