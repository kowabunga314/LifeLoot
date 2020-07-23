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
    context['user_username'] = response.json()['username']
    context['user_email'] = response.json()['email']

def test_login_user():
    body = {'username': 'wumbo', 'password': 'password'}
    response = client.post('/token', body)
    assert response.status_code == 200
    context['access_token'] = response.json()['access_token']
    context['headers'] = {'Authorization': f"Bearer {context['access_token']}"}

def test_get_user_by_id():
    response = client.get(f"/users/{context.get('user_id', 1)}")
    assert response.status_code == 404

def test_get_user_by_username():
    response = client.get(f"/users/{context.get('user_username', 'wumbo')}")
    assert response.status_code == 200
    assert response.json() == {
        "email": "foo@bar",
        "username": "wumbo",
        "id": 1,
        "active": True
    }

def test_get_user_by_email():
    response = client.get(f"/users/{context.get('user_email', 'foo@bar')}")
    assert response.status_code == 404

def test_read_users():
    response = client.get("/users/", headers=context['headers'])
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
