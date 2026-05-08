import pytest
from fastapi.testclient import TestClient
from main import app
from app.state import AppState
from app.loader import load_titulos
from app.dependencies import get_db


@pytest.fixture(scope="session")
def _titulos():
    return load_titulos()


@pytest.fixture(scope="session", autouse=True)
def _preload_app_state(_titulos):
    app.state.db = AppState(titulos=_titulos)


@pytest.fixture
def client(_titulos):
    fresh_db = AppState(titulos=_titulos)
    app.dependency_overrides[get_db] = lambda: fresh_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
