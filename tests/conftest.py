"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from zanything.app import app


@pytest.fixture
def client() -> TestClient:
    """Provide a FastAPI test client."""
    return TestClient(app)
