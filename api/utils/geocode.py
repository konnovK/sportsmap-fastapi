# """
# Функции для работы с геокодером (Yandex API).
# """
#
#
# import asyncio
# import random
#
# import aiohttp
# from loguru import logger
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
#
# from db import Facility
#
#
# async def _get_coords_from_address(address: str, auth: str):
#     """
#     Посылает запрос в геокодер, пытаясь найти координаты для адреса `address`.
#     Требует apikey `auth`.
#
#     https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html?from=mapsapi
#     """
#     async with aiohttp.ClientSession() as session:
#         url = f'https://geocode-maps.yandex.ru/1.x/?apikey={auth}&format=json&geocode={address}'
#         async with session.get(url) as resp:
#             if resp.status != 200:
#                 return None
#             data = await resp.json()
#             logger.debug(f'GEOCODER: RESPONSE FOR {address} | {data}')
#             try:
#                 coords = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
#                 y, x = coords.split(' ')
#                 return x, y
#             except Exception as err:
#                 logger.warning(f'GEOCODER: ERROR FOR {address} | {type(err)}')
#                 return None
#
#
# async def _get_coords_from_address_retry(address: str, auth: str, times=3, sleep_sec=1):
#     """
#     Посылает запрос в геокодер, пытаясь найти координаты для адреса `address`.
#     Требует apikey `auth`.
#
#     Ретраит запросы `times` раз, ожидая между каждым запросом `sleep_sec` секунд.
#
#     https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html?from=mapsapi
#     """
#
#     logger.debug(f'get_coords_from_address_retry: {address}')
#     await asyncio.sleep(random.randint(0, 100) / 1000)
#     res = await _get_coords_from_address(address, auth)
#     if res is None:
#         if times <= 0:
#             return None
#         else:
#             await asyncio.sleep(sleep_sec)
#             times = times - 1
#             return await _get_coords_from_address_retry(address, auth, times)
#     else:
#         return res
#
#
# async def set_facility_coords(
#         async_session: async_sessionmaker[AsyncSession],
#         facility_id: str,
#         address: str,
#         auth: str
# ):
#     """
#     Обновляет объект с id `facility_id`,
#     пытаясь узнать через геокодер координаты для адреса `address`.
#     Для доступа к геокодеру использует apikey `auth`.
#
#     https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html?from=mapsapi
#     """
#     await asyncio.sleep(random.randint(500, 10000) / 1000)
#     address = address.split('(')
#     if len(address) > 1:
#         address = ''.join(address[:-1])
#     else:
#         address = ''.join(address)
#     address = f'г. Санкт-Петербург, {address}'
#     logger.debug(f'GEOCODER: START FOR {address}')
#     async with async_session() as session:
#         facility = await Facility.get_by_id(session, facility_id)
#         if facility is None:
#             logger.debug('facility with this id is not existed')
#             return False
#         facility.x = -1
#         facility.y = -1
#         await session.commit()
#
#         res = await _get_coords_from_address_retry(address, auth)
#         if res is None:
#             logger.debug(f'GEOCODER: FAIL FOR {address}')
#             return False
#         x, y = res
#         x, y = float(x), float(y)
#
#         logger.debug(f'GEOCODER: SUCCESS FOR {address} | ({x};{y})')
#
#         facility = await Facility.get_by_id(session, facility_id)
#         if facility is None:
#             logger.debug('facility with this id is not existed')
#             return False
#         facility.x = x
#         facility.y = y
#         await session.commit()
#
#     return True
#
#
# __all__ = [
#     set_facility_coords
# ]
