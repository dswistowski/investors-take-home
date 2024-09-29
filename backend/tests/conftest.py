import os

import pytest
from fastapi.testclient import TestClient

from backend.app import app


@pytest.fixture(autouse=True)
def _ensure_db_url():
    old_db_url = os.environ.get("DB_URL")
    os.environ["DB_URL"] = os.environ.get(
        "TEST_DB_URL", "postgresql://investors:password@localhost/investors"
    )
    yield
    if old_db_url:
        os.environ["DB_URL"] = old_db_url
    else:
        os.environ.pop("DB_URL")


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
