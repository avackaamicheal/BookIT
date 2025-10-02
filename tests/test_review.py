
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

@pytest.fixture
def completed_booking_with_review(client: TestClient, test_user, test_service):
    user_login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    user_access_token = user_login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_access_token}"}

    start_time = datetime.utcnow() - timedelta(days=5)
    end_time = start_time + timedelta(hours=2)

    booking_data = {
        "service_id": test_service["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    create_booking_response = client.post("/bookings/", json=booking_data, headers=user_headers)
    booking_id = create_booking_response.json()["id"]

    client.patch(f"/bookings/{booking_id}/complete", headers=user_headers)

    review_data = {"booking_id": booking_id, "rating": 5, "comment": "Initial review"}
    create_review_response = client.post("/reviews/", json=review_data, headers=user_headers)
    review_id = create_review_response.json()["id"]

    return client, user_headers, review_id

def test_create_review_for_completed_booking(client: TestClient, test_user, test_service):
    user_login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    user_access_token = user_login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_access_token}"}

    start_time = datetime.utcnow() - timedelta(days=2)
    end_time = start_time + timedelta(hours=2)

    booking_data = {
        "service_id": test_service["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    create_booking_response = client.post("/bookings/", json=booking_data, headers=user_headers)
    booking_id = create_booking_response.json()["id"]

    client.patch(f"/bookings/{booking_id}/complete", headers=user_headers)

    review_data = {"booking_id": booking_id, "rating": 5, "comment": "Excellent service!"}
    create_review_response = client.post("/reviews/", json=review_data, headers=user_headers)
    assert create_review_response.status_code == 200
    assert create_review_response.json()["rating"] == 5

def test_create_review_for_incomplete_booking(client: TestClient, test_user, test_service):
    user_login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    user_access_token = user_login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_access_token}"}

    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)

    booking_data = {
        "service_id": test_service["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    create_booking_response = client.post("/bookings/", json=booking_data, headers=user_headers)
    booking_id = create_booking_response.json()["id"]

    review_data = {"booking_id": booking_id, "rating": 5, "comment": "Should not work"}
    create_review_response = client.post("/reviews/", json=review_data, headers=user_headers)
    assert create_review_response.status_code == 400
    assert "Booking is not completed" in create_review_response.json()["detail"]

def test_update_review_as_owner(completed_booking_with_review):
    client, user_headers, review_id = completed_booking_with_review

    update_data = {"rating": 4, "comment": "It was okay."}
    response = client.patch(f"/reviews/{review_id}", json=update_data, headers=user_headers)
    assert response.status_code == 200
    assert response.json()["rating"] == 4
    assert response.json()["comment"] == "It was okay."

def test_delete_review_as_owner(completed_booking_with_review):
    client, user_headers, review_id = completed_booking_with_review

    response = client.delete(f"/reviews/{review_id}", headers=user_headers)
    assert response.status_code == 200

def test_delete_review_as_admin(client: TestClient, test_user, test_admin, test_service):
    user_login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    user_access_token = user_login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_access_token}"}

    start_time = datetime.utcnow() - timedelta(days=6)
    end_time = start_time + timedelta(hours=2)

    booking_data = {
        "service_id": test_service["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    create_booking_response = client.post("/bookings/", json=booking_data, headers=user_headers)
    booking_id = create_booking_response.json()["id"]

    client.patch(f"/bookings/{booking_id}/complete", headers=user_headers)

    review_data = {"booking_id": booking_id, "rating": 1, "comment": "Horrible!"}
    create_review_response = client.post("/reviews/", json=review_data, headers=user_headers)
    review_id = create_review_response.json()["id"]

    admin_login_response = client.post("/auth/token", data={"username": test_admin["email"], "password": "password"})
    admin_access_token = admin_login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_access_token}"}

    response = client.delete(f"/reviews/{review_id}", headers=admin_headers)
    assert response.status_code == 200
