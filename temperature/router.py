from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud
from dependencies import get_db, Pagination, pagination_params
from temperature.schemas import TemperatureRead

router = APIRouter()


class UpdateTemperaturesResponse(BaseModel):
    message: str
    updated: int
    unupdated: int = 0
    error: list[str] = []


@router.get("/temperatures", response_model=list[TemperatureRead])
async def list_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[Pagination, Depends(pagination_params)],
    city_id: int | None = None,
):
    if city_id:
        temperature = await crud.get_temperature_by_city_id(db=db, city_id=city_id)
        if temperature is None:
            raise HTTPException(
                status_code=404, detail="Temperature for this city not found"
            )
        return temperature

    return await crud.get_all_temperatures(
        db=db, skip=pagination.skip, limit=pagination.limit
    )


@router.post("/temperatures/update")
async def update_all_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UpdateTemperaturesResponse:
    updated_count, errors = await crud.update_all_temperatures(db=db)

    return UpdateTemperaturesResponse(
        message="Temperatures updated successfully",
        updated=updated_count,
        unupdated=len(errors),
        error=errors,
    )
