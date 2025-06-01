import requests

from app import logger


def request_api(url: str) -> dict:
    """Отправка запроса в api погоды"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Ошибка при выполнении запроса: {e}")
        return None


def get_coords_by_name_city(city_name: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=ru"
    response = request_api(url)
    if response is None:
        return
    result = response.get("results", [])
    result = result[0]
    lat, lon = result.get("latitude"), result.get("longitude")
    return lat, lon


def get_weather(city: str):
    """
    Пример ответа
    {
    "time": "2025-06-01T16:45",
    "interval": 900,
    "temperature_2m": 23.5,
    "apparent_temperature": 23.3,
    "is_day": 0,
    "precipitation": 0.0,
    "wind_speed_10m": 4.8,
    "city": "Екатеринбург",
    }
    """
    coords_city = get_coords_by_name_city(city)
    if coords_city is None:
        logger.info("Координаты не полученны")
        return

    weather_criteria = "current=temperature_2m,apparent_temperature,is_day,precipitation,wind_speed_10m"
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={coords_city[0]}&longitude={coords_city[1]}&{weather_criteria}"

    result = request_api(weather_url)

    weather_data = result.get("current")
    weather_data["city"] = city

    return weather_data
