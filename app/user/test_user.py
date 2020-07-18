from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
import json


client = TestClient(app)

context = {}

def test_create_user():
    user = {
        'username': 'wumbo',
        'email': 'foo@bar',
        'password': 'password'
    }
    response = client.post('/users/signup', json.dumps(user))
    assert response.status_code == 200
    assert response.json() == {
        "email": "foo@bar",
        "username": "wumbo",
        "id": 1,
        "active": True
    }
    context['user_id'] = response.json()['id']

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

def test_delete_user():
    response = client.delete(f"/users/{context.get('user_id', 1)}")
    assert response.status_code == 200
