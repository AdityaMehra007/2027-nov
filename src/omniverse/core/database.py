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
        try:
            import omniverse.modules.revenue.models
            import omniverse.modules.commerce.models
            import omniverse.modules.markets.models
            import omniverse.modules.opportunities.models
            import omniverse.modules.aether.models
            import omniverse.modules.planetary_mesh.models
            import omniverse.modules.intelligence.models
            import omniverse.modules.bangalore.models
            import omniverse.modules.bangalore.banking
        except Exception:
            pass
        SQLModel.metadata.create_all(self.engine)

        # Reconcile schema: automatically add missing columns for existing tables (e.g. SQLite migrations)
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(self.engine)
            existing_tables = set(inspector.get_table_names())
            with self.engine.connect() as conn:
                for table_name, table in SQLModel.metadata.tables.items():
                    if table_name in existing_tables:
                        existing_cols = {col["name"] for col in inspector.get_columns(table_name)}
                        for col in table.columns:
                            if col.name not in existing_cols:
                                col_type = col.type.compile(self.engine.dialect)
                                default_clause = ""
                                if col.default is not None and hasattr(col.default, "arg") and not callable(col.default.arg):
                                    default_clause = f" DEFAULT '{col.default.arg}'"
                                conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col.name} {col_type}{default_clause}"))
                                conn.commit()
                # Ensure leads with null uuid get a generated uuid
                if "leads" in existing_tables:
                    conn.execute(text("UPDATE leads SET uuid = lower(hex(randomblob(16))) WHERE uuid IS NULL OR uuid = ''"))
                    conn.commit()
        except Exception:
            pass

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
