import os
from sqlalchemy import QueuePool, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


DB_NAME = "site.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"


def create_db_engine() -> create_engine:
    """
    Создает и возвращает движок SQLAlchemy с настроенным пулом соединений.

    Returns:
        create_engine: Настроенный экземпляр движка SQLAlchemy
    """
    return create_engine(
        SQLALCHEMY_DATABASE_URI,
        poolclass=QueuePool,  # Используем пул соединений
        pool_size=5,  # Максимальное количество соединений в пуле
        max_overflow=10,  # Дополнительные соединения при нагрузке
        pool_timeout=30,  # Время ожидания соединения (сек)
        pool_recycle=3600,  # Пересоздавать соединения каждые час
        connect_args={"check_same_thread": False},  # Для SQLite в многопоточном режиме
        echo=False,  # Логировать SQL-запросы (True для отладки)
    )


engine = create_db_engine()


def create_session_factory() -> sessionmaker:
    """
    Создает фабрику сессий SQLAlchemy.

    Returns:
        sessionmaker: Настроенная фабрика сессий
    """
    return sessionmaker(bind=engine, autoflush=True, autocommit=False, expire_on_commit=True)


Session = create_session_factory()


def get_db():
    """
    Генератор для получения сессии БД в контексте запроса.
    Автоматически закрывает сессию после использования.

    Yields:
        scoped_session: Сессия БД

    Пример работы:
        def some_view():
            db = next(get_db())
            try:
                # работа с БД
            finally:
                db.close()
    """
    db = scoped_session(Session)
    try:
        yield db
    finally:
        db.remove()


db_session = Session()
