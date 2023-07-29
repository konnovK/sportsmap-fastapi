import asyncio

from db.db import DB
from settings import Settings


async def main():
    settings = Settings.new()
    db = DB(settings=settings)
    await db.create_super_user()
    await db.create_all_enums()


if __name__ == '__main__':
    asyncio.run(main())
