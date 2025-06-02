from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, ForeignKey
from app.database.config_db import engine


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""

    pass


class City(Base):
    """Модель города."""

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
        comment="Название города",
    )

    searches: Mapped[list["SearchHistory"]] = relationship(
        "SearchHistory",
        back_populates="city",
        cascade="all, delete-orphan",
    )


class SearchHistory(Base):
    """Модель истории поиска городов."""

    __tablename__ = "search_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID города из таблицы cities",
    )
    count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="Количество поисков этого города",
    )
    last_visited: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Дата последнего посещения",
    )

    # Связь многие-к-одному с городом
    city: Mapped["City"] = relationship("City", back_populates="searches")


def init_db():
    """Инициализация базы данных - создание всех таблиц."""
    Base.metadata.create_all(engine)

init_db()
