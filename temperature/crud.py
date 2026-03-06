import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from integrations.weatherapi import get_temperatures_for_cities
from temperature.models import Temperature
from temperature.schemas import TemperatureRead, TemperatureUpdate


async def get_all_temperatures(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
):
    stmt = select(Temperature).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_temperature_by_city_id(
    db: AsyncSession, city_id: int
) -> TemperatureRead | None:
    stmt = select(Temperature).where(Temperature.city_id == city_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_all_temperatures(db: AsyncSession) -> tuple[int, list[str]]:
    cities_stmt = select(City)
    cities_result = await db.execute(cities_stmt)
    cities = cities_result.scalars().all()

    if not cities:
        return 0, []

    fetched_temperatures, errors = await get_temperatures_for_cities(
        cities=cities, concurrency_limit=10
    )

    existing_temperatures = await db.scalars(select(Temperature))
    existing_temperatures = existing_temperatures.all()

    temperature_by_city_id = {t.city_id: t for t in existing_temperatures}

    for item in fetched_temperatures:
        existing_temperature = temperature_by_city_id.get(item.city_id)
        if existing_temperature:
            existing_temperature.temperature = item.temperature
            existing_temperature.data_time = item.data_time
        else:
            temperature = Temperature(
                city_id=item.city_id,
                temperature=item.temperature,
                data_time=item.data_time,
            )
            db.add(temperature)

    await db.commit()
    return len(cities), errors
