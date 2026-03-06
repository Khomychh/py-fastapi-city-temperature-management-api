from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=511)


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: Optional[str] = None
    description: Optional[str] = None


class TemperatureNestedRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    temperature: float
    data_time: datetime


class CityRead(CityBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    temperature: TemperatureNestedRead | None = None
