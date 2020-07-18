from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_user():
    response = client.post('/users/signup', {
        'username': 'wumbo',
        'email': 'foo@bar',
        'password': 'password'
    })
    assert response.status_code == 200
    assert response.json() == {
        "email": "foo@bar",
        "username": "wumbo",
        "id": 1,
        "active": True
    }

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "email": "foo@bar",
            "username": "wumbo",
            "id": 1,
            "active": True
        }
    ]
