import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from integrations.weatherapi import get_temperature_value
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


async def update_or_create_temperature(db: AsyncSession, city: City) -> None:
    data_task = asyncio.create_task(get_temperature_value(city))

    stmt = select(Temperature).where(Temperature.city_id == city.id)
    temperature = await db.execute(stmt)
    temperature = temperature.scalar_one_or_none()

    try:
        data = await data_task
    except Exception as e:
        raise RuntimeError(
            f"Failed to fetch temperatures from external service. Error: {e}"
        )

    if temperature:
        temperature.temperature = data.temperature
        temperature.data_time = data.data_time
        db.add(temperature)
    else:
        temperature = Temperature(
            city_id=city.id, temperature=data.temperature, data_time=data.data_time
        )
        db.add(temperature)


async def update_all_temperatures(db: AsyncSession) -> int:
    stmt = select(City)
    cities = await db.execute(stmt)
    cities = cities.scalars().all()

    for city in cities:
        await update_or_create_temperature(db=db, city=city)

    await db.commit()
    return len(cities)
