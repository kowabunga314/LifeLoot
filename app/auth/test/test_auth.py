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