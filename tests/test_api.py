import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_api_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Infographic Generator" in response.text
