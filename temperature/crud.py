from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature.models import Temperature
from temperature.schemas import TemperatureRead


async def get_all_temperatures(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
):
    stmt = select(Temperature).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_temperature_by_city_id(db: AsyncSession, city_id: int) -> TemperatureRead | None:
    stmt = select(Temperature).where(Temperature.city_id == city_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()