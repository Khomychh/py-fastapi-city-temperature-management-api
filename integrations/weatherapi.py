import os
import requests

from dotenv import load_dotenv

from city.models import City
from temperature.schemas import TemperatureUpdate

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json?"


async def get_temperature_value(city: City) -> TemperatureUpdate:
    if not API_KEY:
        raise RuntimeError("API key for weatherapi not found")
    try:
        url = f"{BASE_URL}key={API_KEY}&q={city.name}"
        res = requests.get(url).json()
        return TemperatureUpdate(
            city_id=city.id,
            temperature=res["current"]["temp_c"],
            data_time=res["current"]["last_updated"],
        )
    except Exception:
        raise RuntimeError(f"Can't get weather for city with name '{city.name}'")
