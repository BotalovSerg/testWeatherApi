from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import os

Base = declarative_base()


class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)
    count = Column(Integer, default=1)
    last_visited = Column(DateTime, default=datetime.now(timezone.utc))


engine = create_engine(f"sqlite:///{os.path.join(os.path.dirname(__file__), 'site.db')}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
