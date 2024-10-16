from pydantic import BaseModel
from typing import List


class Weather(BaseModel):
    description: str


class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float


class WeatherInfo(BaseModel):
    weather: List[Weather]
    main: Main
