import pytest
from fastapi.testclient import TestClient
from main import app
from db_package.models import Patient, HealthcareProfessional, Caregiver, loginUser

# Assuming you have a test database or a way to mock the database for testing purposes
# You might want to use a testing library for MongoDB like mongomock for this purpose

@pytest.fixture
def test_app():
    return TestClient(app)

def test_read_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "first API"}

def test_get_all_users(test_app):
    response = test_app.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user(test_app):
    user_data = {
        "name": "TestUser",
        "password": "TestPassword",
        "status": "patient",
        "age": 30,
        "memory_score": 80
    }
    response = test_app.post("/create", json=user_data)
    assert response.status_code == 200
    assert response.json()["name"] == "TestUser"
    assert response.json()["status"] == "patient"

def test_login(test_app):
    login_data = {
        "username": "TestUser",
        "password": "TestPassword",
        "status": "patient"
    }
    response = test_app.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_count_patients_above_memory_score(test_app):
    cutoff = 70
    response = test_app.get(f"/api/patients/memory_score/{cutoff}")
    assert response.status_code == 200
    assert isinstance(response.json(), int)

def test_count_patients_above_memory_and_age(test_app):
    memory_cutoff = 70
    age_cutoff = 25
    response = test_app.get(f"/api/patients/memory_age_score/{memory_cutoff}/{age_cutoff}")
    assert response.status_code == 200
    assert isinstance(response.json(), int)
