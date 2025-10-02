from fastapi.testclient import TestClient
from datetime import datetime, timedelta

def test_create_booking(client: TestClient, test_user, test_service):
    login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)

    booking_data = {
        "service_id": test_service["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    response = client.post("/bookings/", json=booking_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["service_id"] == test_service["id"]

def test_create_booking_conflict(client: TestClient, test_user, test_service):
    login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    start_time = datetime.utcnow() + timedelta(days=2)
    end_time = start_time + timedelta(hours=2)

    booking_data = {
        "service_id": test_service["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    # Create the first booking
    response1 = client.post("/bookings/", json=booking_data, headers=headers)
    assert response1.status_code == 200

    # Try to create a conflicting booking
    response2 = client.post("/bookings/", json=booking_data, headers=headers)
    assert response2.status_code == 400
    assert "Booking conflict" in response2.json()["detail"]


def test_delete_booking_as_owner(client: TestClient, test_user, test_service):
    login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    start_time = datetime.utcnow() + timedelta(days=3)
    end_time = start_time + timedelta(hours=2)

    booking_data = {
        "service_id": test_service["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    create_response = client.post("/bookings/", json=booking_data, headers=headers)
    booking_id = create_response.json()["id"]

    delete_response = client.delete(f"/bookings/{booking_id}", headers=headers)
    assert delete_response.status_code == 200


def test_delete_booking_as_admin(client: TestClient, test_user, test_admin, test_service):
    # User creates a booking
    user_login_response = client.post("/auth/token", data={"username": test_user["email"], "password": "password"})
    user_access_token = user_login_response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_access_token}"}

    start_time = datetime.utcnow() + timedelta(days=4)
    end_time = start_time + timedelta(hours=2)

    booking_data = {
        "service_id": test_service["id"],
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }
    create_response = client.post("/bookings/", json=booking_data, headers=user_headers)
    booking_id = create_response.json()["id"]

    # Admin deletes the booking
    admin_login_response = client.post("/auth/token", data={"username": test_admin["email"], "password": "password"})
    admin_access_token = admin_login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_access_token}"}

    delete_response = client.delete(f"/bookings/{booking_id}", headers=admin_headers)
    assert delete_response.status_code == 200
