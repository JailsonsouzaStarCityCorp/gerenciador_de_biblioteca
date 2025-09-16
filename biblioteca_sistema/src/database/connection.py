from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os
from pathlib import Path


class DatabaseConnection:
    def __init__(self, db_path: str | None = None) -> None:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            # Use remote or custom database URL
            self.db_path = None
            self.engine = create_engine(database_url, echo=False, pool_pre_ping=True)
        else:
            if db_path is None:
                project_root = Path(__file__).parent.parent.parent
                db_path = project_root / "database" / "biblioteca.db"
            self.db_path = str(db_path)
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    def close_connection(self) -> None:
        self.engine.dispose()

    def get_db_path(self) -> str | None:
        return self.db_path

    def database_exists(self) -> bool:
        if self.db_path is None:
            # For remote DBs we cannot easily check file existence
            return True
        return os.path.exists(self.db_path)


db_connection = DatabaseConnection()


