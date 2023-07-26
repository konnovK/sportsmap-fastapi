import ssl

from db.schema import metadata
from settings import Settings

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


class DB:
    def __init__(self, settings: Settings):
        self.settings = settings

        db_conn_str = settings.API_DB_URL

        connect_args = {}
        if settings.API_DB_USE_SSL:
            connect_args["ssl"] = ssl.create_default_context(cafile='./CA.pem')

        self.engine = create_async_engine(
            db_conn_str,
            connect_args=connect_args,
            pool_size=20
        )
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_super_user(self):
        if self.settings.API_SUPERUSER_EMAIL is not None and self.settings.API_SUPERUSER_PASSWORD is not None:
            async with self.async_session() as session:
                from db.model.user import User
                try:
                    await User.create(session, {
                        'email': self.settings.API_SUPERUSER_EMAIL,
                        'password': self.settings.API_SUPERUSER_PASSWORD,
                        'admin': True
                    })
                    await session.commit()
                except Exception:
                    pass

    async def create_all_enums(self):
        facility_types = [
            'Плоскостные',
            'Спортивные залы',
            'Бассейны',
            'Крытые катки',
            'Стрелковые объекты',
            'Рекреационные',
            'Другие',
        ]
        facility_owning_types = [
            'Субъект РФ',
            'Муниципальная',
            'Федеральная',
            'Другая',
        ]
        facility_covering_types = [
            'Спротивный линолеум',
            'Ковролин',
            'Спортивный паркет',
            'Деревянный паркет',
            'Бесшовные полиуретановые полы',
            'Рулонные покрытия',
            'Искусственная трава',
            'Гравийное',
            'Искусственный газон',
            'Травяное',
            'Резиновое',
            'Бетонное',
            'Асфальт',
            'Другое',
        ]
        facility_paying_types = [
            'Платные',
            'Бюджетные',
        ]
        facility_ages = [
            'Дети',
            'Молодёжь',
            'Взрослые',
            'Пенсионеры',
        ]
        async with self.async_session() as session:
            try:
                from db.model.facility import FacilityType
                for f in facility_types:
                    f = f.lower()
                    await FacilityType.get_or_create(session, f)

                from db.model.facility import FacilityOwningType
                for f in facility_owning_types:
                    f = f.lower()
                    await FacilityOwningType.get_or_create(session, f)

                from db.model.facility import FacilityCoveringType
                for f in facility_covering_types:
                    f = f.lower()
                    await FacilityCoveringType.get_or_create(session, f)

                from db.model.facility import FacilityPayingType
                for f in facility_paying_types:
                    f = f.lower()
                    await FacilityPayingType.get_or_create(session, f)

                from db.model.facility import FacilityAge
                for f in facility_ages:
                    f = f.lower()
                    await FacilityAge.get_or_create(session, f)

                await session.commit()
            except Exception:
                pass

    async def recreate_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)
