from typing import Optional, Tuple
import requests

from app.logger import logger

DEFAULT_LANGUAGE = "ru"
API_TIMEOUT = 10


def request_api(url: str) -> dict:
    """Отправка запроса в api погоды"""
    try:
        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Ошибка при выполнении запроса: {e}")
        return None


def get_coords_by_name_city(city_name: str) -> Optional[Tuple[float, float]]:
    """
    Получает координаты города по его названию.

    Args:
        city_name (str): Название города

    Returns:
        Optional[Tuple[float, float]]: Кортеж (широта, долгота) или None в случае ошибки
    """

    url = (
        f"https://geocoding-api.open-meteo.com/v1/search?"
        f"name={city_name}"
        f"&count=1"
        f"&language={DEFAULT_LANGUAGE}"
    )
    logger.debug(f"Запрос координат для города: {city_name}")

    response = request_api(url)

    if response is None:
        logger.error(f"Не удалось получить координаты для города: {city_name}")
        return None

    results = response.get("results")
    if not results or len(results) == 0:
        logger.info(f"Город не найден: {city_name}")
        return None

    location = results[0]
    lat = location.get("latitude")
    lon = location.get("longitude")

    if lat is None or lon is None:
        logger.error(f"Неполные координаты в ответе: {location}")
        return None

    return lat, lon


def get_weather(city: str) -> Optional[dict]:
    """
    Получает текущую погоду для указанного города.

    Args:
        city (str): Название города

    Returns:
        Optional[dict]: Словарь с данными о погоде или None в случае ошибки

    Пример возвращаемого значения:
        {
            "time": "2025-06-01T16:45",
            "temperature_2m": 23.5,
            "apparent_temperature": 23.3,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 4.8,
            "precipitation": 0.0,
            "surface_pressure": 1012.5,
            "city": "Екатеринбург",
        }
    """
    coords_city = get_coords_by_name_city(city)

    if coords_city is None:
        logger.info("Координаты не полученны")
        return None

    weather_params = [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "wind_speed_10m",
        "precipitation",
        "surface_pressure",
    ]

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={coords_city[0]}"
        f"&longitude={coords_city[1]}"
        f"&current={','.join(weather_params)}"
        f"&timezone=auto"
    )

    result = request_api(url)
    if not result:
        logger.error(f"Не удалось получить погоду для города: {city}")
        return None

    weather_data = result.get("current")
    weather_data["city"] = city

    return weather_data
