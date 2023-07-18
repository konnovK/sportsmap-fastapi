import os
import time

import pandas as pd
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from service.model.excel_model import FacilityExcelItemServiceModel

from db.model.facility import Facility


class ExcelController:
    def __init__(self, async_session):
        self.async_session = async_session

    _db_fields = {
        'Наименование': 'name',
        'Адрес': 'address',
        'Пользователь': 'owner',
        'Форма собственности': 'owning_type',

        'Длина': 'length',
        'Ширина': 'width',
        'Высота': 'height',
        'Глубина': 'depth',

        'Площадь': 'area',

        'ЕПС': 'eps',
        'Фактическая загруженность': 'actual_workload',
        'Годовая мощность': 'annual_capacity',

        'Покрытие': 'covering_type',

        'Документ': 'document',
        'Примечания': 'note',
        '№': 'n',
    }

    _readable_fields = {
        'name': 'Наименование',
        'address': 'Адрес',
        'owner': 'Пользователь',
        'owning_type': 'Форма собственности',

        'length': 'Длина',
        'width': 'Ширина',
        'height': 'Высота',
        'depth': 'Глубина',

        'area': 'Площадь',

        'eps': 'ЕПС',
        'actual_workload': 'Фактическая загруженность',
        'annual_capacity': 'Годовая мощность',

        'covering_type': 'Покрытие',

        'document': 'Документ',
        'note': 'Примечания',
    }

    def xls_to_list(self, xls) -> list[dict]:
        """
        Makes list of facility dicts from pandas xls object.
        """
        facilities = []
        f_types = xls.keys()
        for f_type in f_types:
            df = xls[f_type]
            df_size = len(df.values)
            df_fields = df.keys()
            for i in range(1, df_size):
                obj = df.iloc[i]
                obj_dict = {}
                for j in range(0, len(df_fields)):
                    try:
                        if str(obj[j]) == 'nan':  # костыль, проверка числа на пандасовский NaN
                            continue
                        obj_dict[self._db_fields[df_fields[j]]] = obj[j]
                    except KeyError:
                        pass
                obj_dict['type'] = f_type
                facilities.append(obj_dict)
        return facilities

    def validate_excel_facilities(self, facilities: list[dict]) -> list[dict]:
        """
        Validate facilities and return list of ValidationErrors
        """
        errors = []
        for facility in facilities:
            try:
                n = int(facility.pop('n'))
            except KeyError:
                n = None
            try:
                FacilityExcelItemServiceModel.model_validate(facility)
            except ValidationError as err:
                err: ValidationError
                errors.append({
                    'n': n,
                    'type': str(facility.get('type')),
                    'name': str(facility.get('name')),
                    'detail': err.json(),
                })
        return errors

    def _facility_to_human_readable(self, facility: dict):
        """
        В словаре `facility` меняет ключи на человекочитаемые русские аналоги.

        Типа name -> Наименование.

        Типа actual_workload -> Фактическая загруженность.
        """
        readable_facility = {}
        for k, v in facility.items():
            if k in self._readable_fields and v is not None:
                readable_facility[self._readable_fields[k]] = v

        return readable_facility

    async def _add_excel_facility_to_db(self, session: AsyncSession, facility: dict):
        f = FacilityExcelItemServiceModel.model_validate(facility).model_dump()
        if f.get('document') is not None:
            f['document'] = str(f['document'])
        await session.begin_nested()
        f_db = await Facility.construct(session, f)
        session.add(f_db)
        await session.commit()
        return {
            "id": f_db.id,
            "address": f_db.address
        }

    async def add_excel_facilities_to_db(self, async_session, facilities: list[dict]):
        # logger.debug(f'TRY TO IMPORT {len(facilities)} FACILITIES FROM EXCEL TO DB')
        async with async_session() as session:
            session: AsyncSession
            facilities_in_db = []
            for facility in facilities:
                try:
                    _ = facility.pop('n')
                except KeyError:
                    pass
                start = time.time()
                try:
                    logger.debug(f'ADD: TRY TO ADD FACILITY')
                    f_db = await self._add_excel_facility_to_db(session, facility)
                    logger.debug(f'SUCCESS: ADD FACILITY {time.time() - start : 0.3f}MS: f{f_db.get("id")}')
                    facilities_in_db.append(f_db)
                except DataError:
                    logger.debug(f'ERROR: {time.time() - start : 0.3f}MS: DataError')
                    await session.rollback()
                except IntegrityError:
                    logger.debug(f'ERROR: {time.time() - start : 0.3f}MS: IntegrityError')
                    await session.rollback()
            await session.commit()
            return facilities_in_db

    def _facilities_to_df_by_type(self, facilities: list):
        facility_by_types = {}

        # линия
        for f in facilities:
            f_type = f['type']
            f = self._facility_to_human_readable(f)
            if facility_by_types.get(f_type) is None:
                facility_by_types[f_type] = [f, ]
            else:
                facility_by_types[f_type].append(f)

        df_by_type = {}

        for f_type in facility_by_types:
            df = pd.DataFrame(facility_by_types[f_type])
            df_by_type[f_type] = df
        return df_by_type

    def create_excel_file(self, excel_filename: str, facilities: list):
        df_by_type = self._facilities_to_df_by_type(facilities)
        try:
            os.remove(excel_filename)
        except Exception:
            pass
        with pd.ExcelWriter(excel_filename) as writer:
            for f_type in df_by_type:
                df: pd.DataFrame = df_by_type[f_type]
                df.to_excel(writer, f_type)
