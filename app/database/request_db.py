from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from .models import SearchHistory, City

from app.logger import logger


def get_city_by_name(db: Session, city_name: str) -> Optional[City]:
    """
    Получает город из базы данных по его названию.

    Args:
        db (Session): Сессия базы данных SQLAlchemy
        city_name (str): Название города для поиска

    Returns:
        Optional[City]: Объект города или None, если город не найден
    """
    logger.debug(f"Поиск города по имени: {city_name}")
    city = db.query(City).filter(City.name == city_name).first()

    if not city:
        logger.debug(f"Город {city_name} не найден в базе")
    else:
        logger.debug(f"Найден город: {city.name} (ID: {city.id})")

    return city


def create_city(db: Session, city_name: str) -> City:
    """
    Создает новую запись города в базе данных.

    Args:
        db (Session): Сессия базы данных SQLAlchemy
        city_name (str): Название создаваемого города

    Returns:
        City: Созданный объект города

    Raises:
        Exception: В случае ошибки при создании города
    """
    logger.info(f"Создание нового города: {city_name}")
    try:
        city = City(name=city_name)
        db.add(city)
        db.flush()
        db.commit()
        logger.info(f"Успешно создан город {city_name} (ID: {city.id})")
        return city
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при создании города {city_name}: {str(e)}")
        raise


def get_or_create_city(db: Session, city_name: str) -> City:
    """
    Получает город из базы или создает новый, если он не существует.

    Args:
        db (Session): Сессия базы данных SQLAlchemy
        city_name (str): Название города

    Returns:
        City: Существующий или созданный объект города
    """
    logger.debug(f"Попытка получить или создать город: {city_name}")
    city = get_city_by_name(db, city_name)

    if not city:
        logger.info(f"Город {city_name} не найден, создаем новый")
        city = create_city(db, city_name)

    return city


def get_search_history_by_city_id(db: Session, city_id: int) -> Optional[SearchHistory]:
    """
    Получает историю поиска по ID города.

    Args:
        db (Session): Сессия базы данных SQLAlchemy
        city_id (int): ID города для поиска в истории

    Returns:
        Optional[SearchHistory]: Запись истории поиска или None, если не найдена
    """
    logger.debug(f"Поиск истории для города с ID: {city_id}")
    history_entry = db.query(SearchHistory).filter(SearchHistory.city_id == city_id).first()

    if history_entry:
        logger.debug(f"Найдена запись истории для города ID {city_id}: {history_entry.count} посещений")
    else:
        logger.debug(f"История для города ID {city_id} не найдена")

    return history_entry


def update_or_create_search_history(db: Session, city_id: int) -> SearchHistory:
    """
    Обновляет счетчик посещений для существующей записи истории или создает новую.

    Args:
        db (Session): Сессия базы данных SQLAlchemy
        city_id (int): ID города для обновления истории

    Returns:
        SearchHistory: Обновленная или созданная запись истории

    Raises:
        Exception: В случае ошибки при обновлении/создании записи
    """
    logger.info(f"Обновление истории поиска для города ID: {city_id}")
    try:
        history_entry = get_search_history_by_city_id(db, city_id)

        if history_entry:
            history_entry.count += 1
            history_entry.last_visited = datetime.now(timezone.utc)
            logger.debug(f"Обновлена запись истории: теперь {history_entry.count} посещений")
        else:
            history_entry = SearchHistory(city_id=city_id, last_visited=datetime.now(timezone.utc), count=1)
            db.add(history_entry)
            logger.debug("Создана новая запись истории поиска")

        db.commit()
        return history_entry
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при обновлении истории поиска для города ID {city_id}: {str(e)}")
        raise


def get_all_search_stats(db: Session) -> List[Tuple[str, int, datetime]]:
    """
    Получает статистику поиска по всем городам.

    Args:
        db (Session): Сессия базы данных SQLAlchemy

    Returns:
        List[Tuple[str, int, datetime]]: Список кортежей с:
            - названием города
            - количеством посещений
            - датой последнего посещения
    """
    logger.debug("Получение статистики поиска по городам")
    stats = (
        db.query(City.name, SearchHistory.count, SearchHistory.last_visited)
        .join(SearchHistory, City.id == SearchHistory.city_id)
        .all()
    )
    logger.debug(f"Получено {len(stats)} записей статистики")
    return stats


def get_cities_by_prefix(db: Session, prefix: str, limit: int = 5) -> List[str]:
    """
    Получает список городов, названия которых начинаются с заданного префикса.

    Args:
        db (Session): Сессия базы данных SQLAlchemy
        prefix (str): Префикс для поиска городов
        limit (int): Максимальное количество возвращаемых результатов

    Returns:
        List[str]: Список названий городов, соответствующих префиксу
    """
    logger.debug(f"Поиск городов по префиксу: '{prefix}' (лимит: {limit})")

    if not prefix:
        logger.debug("Пустой префикс, возвращаем пустой список")
        return []

    results = db.query(City.name).filter(City.name.ilike(f"{prefix}%")).limit(limit).all()
    cities = [row.name for row in results]

    logger.debug(f"Найдено {len(cities)} городов по префиксу '{prefix}'")
    return cities
