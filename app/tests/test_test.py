"""Example pytest tests"""
from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_answer():
    """Example test use case"""

    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}



   
