from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker
from models import Base  # Импортируем Base из models.py
from typing import Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///normative_docs.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
inspector = inspect(engine)
metadata = MetaData()

Base.metadata.create_all(bind=engine)
metadata.reflect(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_db_table_names():
    table_names = inspector.get_table_names()

    # Получаем информацию о столбцах конкретной таблицы
    for table_name in table_names:
        print(f"Таблица: {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            print(f"  Столбец: {column['name']} ({column['type']})")

def get_db_table_metadata():
    for table in metadata.sorted_tables:
        print(f"Таблица: {table.name}")
        for column in table.columns:
            print(f"  {column.name}: {column.type}")
        print("  Индексы:")
        for index in table.indexes:
            print(f"    {index.name}: {index.columns}")
        print("  Ограничения:")
        for constraint in table.constraints:
            print(f"    {constraint.name}: {constraint}")
