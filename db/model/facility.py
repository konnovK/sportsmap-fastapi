import datetime
import uuid
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DataError

from db.schema import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.sql import func

facility_facility_paying_type_association_table = sa.Table(
    "facility_facility_paying_type_association_table",
    Base.metadata,
    sa.Column("facility", sa.ForeignKey("facility.id")),
    sa.Column("facility_paying_type", sa.ForeignKey("facility_paying_type.name")),
)

facility_facility_age_association_table = sa.Table(
    "facility_facility_age_association_table",
    Base.metadata,
    sa.Column("facility", sa.ForeignKey("facility.id")),
    sa.Column("facility_age", sa.ForeignKey("facility_age.name")),
)

facility_facility_photo_association_table = sa.Table(
    "facility_facility_photo_association_table",
    Base.metadata,
    sa.Column("facility", sa.ForeignKey("facility.id")),
    sa.Column("facility_photo", sa.ForeignKey("facility_photo.id")),
)


class FacilityPayingType(Base):
    __tablename__ = 'facility_paying_type'
    name: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, nullable=False)
    facilities = so.relationship(
        "Facility",
        secondary=facility_facility_paying_type_association_table,
        back_populates='paying_type', lazy='selectin'
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    async def get(session: AsyncSession, name: str):
        facility_paying_type = (
            await session.execute(
                sa.select(FacilityPayingType)
                .where(FacilityPayingType.name == name)
            )
        ).scalars().first()
        return facility_paying_type

    @staticmethod
    async def create(session: AsyncSession, name: str):
        facility_paying_type = FacilityPayingType(name=name)
        session.add(facility_paying_type)
        await session.flush()
        return facility_paying_type

    @staticmethod
    async def get_or_create(session: AsyncSession, name: str):
        facility_paying_type = await FacilityPayingType.get(session, name)
        if facility_paying_type is not None:
            return facility_paying_type
        else:
            facility_paying_type = await FacilityPayingType.create(session, name)
            return facility_paying_type


class FacilityAge(Base):
    __tablename__ = 'facility_age'
    name: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, nullable=False)
    facilities = so.relationship(
        "Facility",
        secondary=facility_facility_age_association_table,
        back_populates='age', lazy='selectin'
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    async def get(session: AsyncSession, name: str):
        facility_age = (
            await session.execute(
                sa.select(FacilityAge)
                .where(FacilityAge.name == name)
            )
        ).scalars().first()
        return facility_age

    @staticmethod
    async def create(session: AsyncSession, name: str):
        facility_age = FacilityAge(name=name)
        session.add(facility_age)
        await session.flush()
        return facility_age

    @staticmethod
    async def get_or_create(session: AsyncSession, name: str):
        facility_age = await FacilityAge.get(session, name)
        if facility_age is not None:
            return facility_age
        else:
            facility_age = await FacilityAge.create(session, name)
            return facility_age


class FacilityType(Base):
    __tablename__ = 'facility_type'
    name: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, nullable=False)
    facilities = so.relationship(
        "Facility",
        back_populates='type', lazy='selectin'
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    async def get(session: AsyncSession, name: str):
        obj = (
            await session.execute(
                sa.select(FacilityType)
                .where(FacilityType.name == name)
            )
        ).scalars().first()
        return obj

    @staticmethod
    async def create(session: AsyncSession, name: str):
        obj = FacilityType(name=name)
        session.add(obj)
        await session.flush()
        return obj

    @staticmethod
    async def get_or_create(session: AsyncSession, name: str):
        obj = await FacilityType.get(session, name)
        if obj is not None:
            return obj
        else:
            obj = await FacilityType.create(session, name)
            return obj


class FacilityOwningType(Base):
    __tablename__ = 'facility_owning_type'
    name: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, nullable=False)
    facilities = so.relationship(
        "Facility",
        back_populates='owning_type', lazy='selectin'
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    async def get(session: AsyncSession, name: str):
        obj = (
            await session.execute(
                sa.select(FacilityOwningType)
                .where(FacilityOwningType.name == name)
            )
        ).scalars().first()
        return obj

    @staticmethod
    async def create(session: AsyncSession, name: str):
        obj = FacilityOwningType(name=name)
        session.add(obj)
        await session.flush()
        return obj

    @staticmethod
    async def get_or_create(session: AsyncSession, name: str):
        obj = await FacilityOwningType.get(session, name)
        if obj is not None:
            return obj
        else:
            obj = await FacilityOwningType.create(session, name)
            return obj


class FacilityCoveringType(Base):
    __tablename__ = 'facility_covering_type'
    name: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, nullable=False)
    facilities = so.relationship(
        "Facility",
        back_populates='covering_type', lazy='selectin'
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    async def get(session: AsyncSession, name: str):
        obj = (
            await session.execute(
                sa.select(FacilityCoveringType)
                .where(FacilityCoveringType.name == name)
            )
        ).scalars().first()
        return obj

    @staticmethod
    async def create(session: AsyncSession, name: str):
        obj = FacilityCoveringType(name=name)
        session.add(obj)
        await session.flush()
        return obj

    @staticmethod
    async def get_or_create(session: AsyncSession, name: str):
        obj = await FacilityCoveringType.get(session, name)
        if obj is not None:
            return obj
        else:
            obj = await FacilityCoveringType.create(session, name)
            return obj


class FacilityPhoto(Base):
    __tablename__ = 'facility_photo'
    id: so.Mapped[uuid.UUID] = so.mapped_column(sa.UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    url: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)
    filename: so.Mapped[str] = so.mapped_column(sa.String, nullable=True)
    facilities = so.relationship(
        "Facility",
        secondary=facility_facility_photo_association_table,
        back_populates='photo', lazy='selectin'
    )

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url

    @staticmethod
    async def get(session: AsyncSession, url: str):
        obj = (
            await session.execute(
                sa.select(FacilityPhoto)
                .where(FacilityPhoto.url == url)
            )
        ).scalars().first()
        return obj

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str):
        try:
            obj = (
                await session.execute(
                    sa.select(FacilityPhoto)
                    .where(FacilityPhoto.id == id)
                )
            ).scalars().first()
            return obj
        except DataError as err:
            logger.debug(err)
            return None

    @staticmethod
    async def create(session: AsyncSession, url: str, filename: str):
        obj = FacilityPhoto(url=url, filename=filename)
        session.add(obj)
        await session.flush()
        return obj

    @staticmethod
    async def get_or_create(session: AsyncSession, url: str, filename: str):
        obj = await FacilityPhoto.get(session, url)
        if obj is not None:
            return obj
        else:
            obj = await FacilityPhoto.create(session, url, filename)
            return obj


class Facility(Base):
    __tablename__ = 'facility'

    id: so.Mapped[uuid.UUID] = so.mapped_column(sa.UUID(), primary_key=True, default=uuid.uuid4, nullable=False)

    x: so.Mapped[float] = so.mapped_column(sa.Float, nullable=True)  # nullable=True ЭТО ВРЕМЕННО, БУДЕТ False
    y: so.Mapped[float] = so.mapped_column(sa.Float, nullable=True)  # nullable=True ЭТО ВРЕМЕННО, БУДЕТ False
    hidden: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=True)

    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    address: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    owner: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)

    length: so.Mapped[float] = so.mapped_column(sa.Float, nullable=True)
    width: so.Mapped[float] = so.mapped_column(sa.Float, nullable=True)
    height: so.Mapped[float] = so.mapped_column(sa.Float, nullable=True)
    depth: so.Mapped[float] = so.mapped_column(sa.Float, nullable=True)
    area: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    eps: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    actual_workload: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    annual_capacity: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)

    accessibility: so.Mapped[bool] = so.mapped_column(sa.Boolean, nullable=False, default=False)

    site: so.Mapped[str] = so.mapped_column(sa.String, nullable=True)
    phone_number: so.Mapped[str] = so.mapped_column(sa.String, nullable=True)
    document: so.Mapped[str] = so.mapped_column(sa.String, nullable=True)
    note: so.Mapped[str] = so.mapped_column(sa.String, nullable=True)

    working_hours: so.Mapped[dict] = so.mapped_column(sa.JSON, nullable=True)

    type_name = so.mapped_column(sa.ForeignKey('facility_type.name'), nullable=False)
    type: so.Mapped[FacilityType] = so.relationship(back_populates='facilities', lazy='selectin')
    owning_type_name = so.mapped_column(sa.ForeignKey("facility_owning_type.name"), nullable=True)
    owning_type: so.Mapped[FacilityOwningType] = so.relationship(back_populates='facilities', lazy='selectin')
    covering_type_name = so.mapped_column(sa.ForeignKey("facility_covering_type.name"), nullable=True)
    covering_type: so.Mapped[FacilityCoveringType] = so.relationship(back_populates='facilities', lazy='selectin')
    paying_type: so.Mapped[list[FacilityPayingType]] = so.relationship(
        "FacilityPayingType",
        secondary=facility_facility_paying_type_association_table,
        back_populates='facilities', lazy='selectin'
    )
    age: so.Mapped[list[FacilityAge]] = so.relationship(
        "FacilityAge",
        secondary=facility_facility_age_association_table,
        back_populates='facilities', lazy='selectin'
    )
    photo: so.Mapped[list[FacilityPhoto]] = so.relationship(
        "FacilityPhoto",
        secondary=facility_facility_photo_association_table,
        back_populates='facilities', lazy='selectin'
    )

    created_at: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now())

    sa.UniqueConstraint(
        name,
        address,
        owner,
        area,
        type_name,
    )

    ix_id = sa.Index('ix__facility__id', id, postgresql_using='hash')
    ix_name = sa.Index('ix__facility__name', name, postgresql_using='hash')
    ix_owner = sa.Index('ix__facility__owner', owner, postgresql_using='hash')
    ix_address = sa.Index('ix__facility__address', address, postgresql_using='hash')
    ix_x = sa.Index('ix__facility__x', x, postgresql_using='btree')
    ix_y = sa.Index('ix__facility__y', y, postgresql_using='btree')

    def __repr__(self):
        return f'Facility(' \
               f'id={self.id} ' \
               f'paying_type={self.paying_type} ' \
               f'type={self.type_name})'

    @staticmethod
    async def create(session: AsyncSession, facility_data: dict):
        try:
            facility_paying_type = facility_data.pop('paying_type')
            if facility_paying_type is None:
                facility_paying_type = []
        except KeyError:
            facility_paying_type = []
        paying_type = []
        for fpt in facility_paying_type:
            fpt = fpt.lower()
            f = await FacilityPayingType.get_or_create(session, fpt)
            paying_type.append(f)
        facility_data['paying_type'] = paying_type

        try:
            facility_age = facility_data.pop('age')
            if facility_age is None:
                facility_age = []
        except KeyError:
            facility_age = []
        age = []
        for fa in facility_age:
            fa = fa.lower()
            f = await FacilityAge.get_or_create(session, fa)
            age.append(f)
        facility_data['age'] = age

        facility_type = facility_data.pop('type')
        facility_type = facility_type.lower()
        type = await FacilityType.get_or_create(session, facility_type)
        facility_data['type'] = type

        if facility_data.get('owning_type') is not None:
            facility_owning_type = facility_data.pop('owning_type')
            facility_owning_type = facility_owning_type.lower()
            owning_type = await FacilityOwningType.get_or_create(session, facility_owning_type)
            facility_data['owning_type'] = owning_type
        else:
            facility_owning_type = 'другая'
            owning_type = await FacilityOwningType.get_or_create(session, facility_owning_type)
            facility_data['owning_type'] = owning_type

        if facility_data.get('covering_type') is not None:
            facility_covering_type = facility_data.pop('covering_type')
            facility_covering_type = facility_covering_type.lower()
            covering_type = await FacilityCoveringType.get_or_create(session, facility_covering_type)
            facility_data['covering_type'] = covering_type

        facility = Facility(**facility_data)
        session.add(facility)
        await session.flush()
        return facility

    @staticmethod
    async def construct(session: AsyncSession, facility_data: dict):
        facility_data['hidden'] = False
        try:
            facility_paying_type = facility_data.pop('paying_type')
        except KeyError:
            facility_paying_type = []
        if facility_paying_type == []:
            facility_paying_type = ['бюджетные']
        paying_type = []
        for fpt in facility_paying_type:
            fpt = fpt.lower()
            f = await FacilityPayingType.get_or_create(session, fpt)
            paying_type.append(f)
        facility_data['paying_type'] = paying_type

        try:
            facility_age = facility_data.pop('age')
        except KeyError:
            facility_age = []
        if facility_age == []:
            facility_age = [
                "взрослые",
                "дети",
                "молодёжь",
                "пенсионеры"
            ]
        age = []
        for fa in facility_age:
            fa = fa.lower()
            f = await FacilityAge.get_or_create(session, fa)
            age.append(f)
        facility_data['age'] = age

        facility_type = facility_data.pop('type')
        facility_type = facility_type.lower()
        type = await FacilityType.get_or_create(session, facility_type)
        facility_data['type'] = type

        if facility_data.get('owning_type') is not None:
            facility_owning_type = facility_data.pop('owning_type')
            facility_owning_type = facility_owning_type.lower()
            owning_type = await FacilityOwningType.get_or_create(session, facility_owning_type)
            facility_data['owning_type'] = owning_type
        else:
            facility_owning_type = 'другая'
            owning_type = await FacilityOwningType.get_or_create(session, facility_owning_type)
            facility_data['owning_type'] = owning_type

        if facility_data.get('covering_type') is not None:
            facility_covering_type = facility_data.pop('covering_type')
            facility_covering_type = facility_covering_type.lower()
            covering_type = await FacilityCoveringType.get_or_create(session, facility_covering_type)
            facility_data['covering_type'] = covering_type

        facility = Facility(**facility_data)
        return facility

    @staticmethod
    async def get_by_id(session: AsyncSession, id: str):
        try:
            facility = (
                await session.execute(
                    sa.select(Facility)
                    .where(Facility.id == id)
                )
            ).scalars().first()
            return facility
        except Exception as e:
            logger.debug(e)
            return None

    @staticmethod
    async def get_all(session: AsyncSession):
        facilities = (
            await session.execute(sa.select(Facility))
        ).scalars().all()
        return facilities

    @staticmethod
    async def count(session: AsyncSession) -> int:
        count = (
            await session.execute(sa.func.count(Facility.id))
        ).scalar()
        return count
