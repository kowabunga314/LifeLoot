from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
import json


client = TestClient(app)

context = {}

def test_create_home_user():
    user = {
        'username': 'home_team',
        'email': 'home@bar',
        'password': 'password'
    }
    response = client.post('/users/signup', json.dumps(user))
    assert response.status_code == 200
    assert response.json() == {
        "email": "home@bar",
        "username": "home_team",
        "id": 1,
        "active": True
    }
    context['home_id'] = response.json()['id']
    context['home_username'] = response.json()['username']
    context['home_email'] = response.json()['email']
    
def test_create_away_user():
    user = {
        'username': 'away_team',
        'email': 'away@bar',
        'password': 'password'
    }
    response = client.post('/users/signup', json.dumps(user))
    assert response.status_code == 200
    assert response.json() == {
        "email": "away@bar",
        "username": "away_team",
        "id": 1,
        "active": True
    }
    context['away_id'] = response.json()['id']
    context['away_username'] = response.json()['username']
    context['away_email'] = response.json()['email']