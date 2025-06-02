from typing import Optional


class InvalidCityError(Exception):
    """Исключение для невалидных названий городов."""
    pass


def validate_city(city: Optional[str]) -> str:
    """
    Валидирует и нормализует название города.

    Параметры:
        city (str): Сырое название города из формы

    Возвращает:
        str: Валидное нормализованное название города

    Исключения:
        InvalidCityError: Если город невалиден
    """
    if not city or not isinstance(city, str):
        raise InvalidCityError("Введите название города.")

    normalized_city = city.strip().capitalize()

    if len(normalized_city) < 2:
        raise InvalidCityError("Название города слишком короткое.")

    if not all(c.isalpha() or c.isspace() or c in "-'" for c in normalized_city):
        raise InvalidCityError("Название города содержит недопустимые символы.")

    return normalized_city
