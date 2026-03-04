from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

router = APIRouter()

@router.get("/temperatures")
async def read_items(db: Annotated[AsyncSession, Depends(get_db)]):
    return {"message": "Hello World"}
