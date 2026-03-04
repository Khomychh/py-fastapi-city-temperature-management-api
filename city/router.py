from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

router = APIRouter()

@router.get("/cities")
async def read_items(db: Annotated[AsyncSession, Depends(get_db)]):
    return {"message": "Hello World"}


@router.post("/cities")
async def create_city(db: Annotated[AsyncSession, Depends(get_db)]):
    return {"message": "Hello World"}


@router.get("/cities/{city_id}")
async def read_city(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return {"city_id": city_id}


@router.put("/cities/{city_id}")
async def update_city(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return {"city_id": city_id, "action": "update"}


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return {"city_id": city_id, "action": "delete"}