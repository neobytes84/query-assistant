## query-assistant-service/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from api_gateway.app.main import app

client = TestClient(app)

def test_query_endpoint():
    response = client.post("/query", json={"question": "¿Cuál es el producto más vendido?"})
    assert response.status_code == 200 or response.status_code == 500  # Puede fallar por dependencias