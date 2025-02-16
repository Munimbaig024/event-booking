from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"username": "testuser", "email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200

def test_login_user():
    response = client.post("/login", json={"email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
