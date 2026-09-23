from fastapi.testclient import TestClient
from devtrack.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "server is running"}