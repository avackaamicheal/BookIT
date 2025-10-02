from fastapi.testclient import TestClient
import pytest

def test_create_user(client: TestClient):
    response = client.post("/users/", json={"email": "newuser@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"

def test_login_for_access_token(client: TestClient, test_user):
    response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_current_user_unauthorized(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 401

def test_get_current_user(client: TestClient, test_user):
    login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
