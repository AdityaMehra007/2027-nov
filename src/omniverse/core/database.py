from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os
from pathlib import Path
from typing import Generator
from omniverse.core.config import get_settings

class DatabaseEngine:
    def __init__(self, db_url: str | None = None):
        self.settings = get_settings()
        self.db_url = db_url or self.settings.db_url
        
        # Ensure parent directory exists for SQLite
        if self.db_url.startswith("sqlite:///"):
            path_part = self.db_url.replace("sqlite:///", "")
            if path_part != ":memory:":
                db_path = Path(path_part)
                db_path.parent.mkdir(parents=True, exist_ok=True)
                
        connect_args = {"check_same_thread": False} if self.db_url.startswith("sqlite") else {}
        self.engine = create_engine(self.db_url, echo=False, connect_args=connect_args)

    def init_db(self) -> None:
        """Create all registered SQLModel tables."""
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        with Session(self.engine) as session:
            yield session

# Global default instance
_default_engine = None

def get_engine() -> DatabaseEngine:
    global _default_engine
    if _default_engine is None:
        _default_engine = DatabaseEngine()
    return _default_engine

@contextmanager
def get_session() -> Generator[Session, None, None]:
    engine = get_engine()
    with engine.get_session() as session:
        yield session

def init_db() -> None:
    get_engine().init_db()
