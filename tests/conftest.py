import pytest
from sqlmodel import Session, SQLModel, create_engine
import os
import tempfile

@pytest.fixture(name="test_db")
def test_db_fixture():
    # Use temporary in-memory sqlite db for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
