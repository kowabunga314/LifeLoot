from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app.game.schema import GameCreate, ScoreUpdate
from app.user.schema import UserCreate
import json


client = TestClient(app)

context = {}

def test_create_home_user():
    user = UserCreate(username='home_team', email='home@bar', password='password')

    response = client.post('/users/signup', json.dumps(user.dict()))
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
    user = UserCreate(username='away_team', email='away@bar', password='password')
    
    response = client.post('/users/signup', json.dumps(user.dict()))
    assert response.status_code == 200
    assert response.json() == {
        "email": "away@bar",
        "username": "away_team",
        "id": 2,
        "active": True
    }
    context['away_id'] = response.json()['id']
    context['away_username'] = response.json()['username']
    context['away_email'] = response.json()['email']

def test_create_game():
    game = GameCreate(home_id=context['home_id'], away_id=context['away_id'])

    response = client.post('/games/', json.dumps(game.dict()))
    assert response.status_code == 200
    assert response.json() == {
        "home_id": 1,
        "home_life": 20,
        "away_id": 2,
        "away_life": 20,
        "title": None,
        "description": None,
        "active": True,
        "id": 1,
        "home_user": {
            "email": "home@bar",
            "username": "home_team",
            "id": 1,
            "active": True
        },
        "away_user": {
            "email": "away@bar",
            "username": "away_team",
            "id": 2,
            "active": True
        }
    }

    context['game_id'] = response.json()['id']

def test_update_home_life():
    update = ScoreUpdate(game_id=context['game_id'], team='home', increment=-2)

    response = client.put(f'/games/{update.game_id}', json.dumps(update.dict()))

    assert response.status_code == 200
    assert response.json() == {
        "home_id": 1,
        "home_life": 18,
        "away_id": 2,
        "away_life": 20,
        "title": None,
        "description": None,
        "active": True,
        "id": 1,
        "home_user": {
            "email": "home@bar",
            "username": "home_team",
            "id": 1,
            "active": True
        },
        "away_user": {
            "email": "away@bar",
            "username": "away_team",
            "id": 2,
            "active": True
        }
    }

def test_update_away_life():
    update = ScoreUpdate(game_id=context['game_id'], team='away', absolute=0)

    response = client.put(f'/games/{update.game_id}', json.dumps(update.dict()))

    assert response.status_code == 200
    assert response.json() == {
        "home_id": 1,
        "home_life": 18,
        "away_id": 2,
        "away_life": 0,
        "title": None,
        "description": None,
        "active": True,
        "id": 1,
        "home_user": {
            "email": "home@bar",
            "username": "home_team",
            "id": 1,
            "active": True
        },
        "away_user": {
            "email": "away@bar",
            "username": "away_team",
            "id": 2,
            "active": True
        }
    }

def test_end_game():
    game_id = context['game_id']
    response = client.put(f'/games/{game_id}/end')

    assert response.status_code == 200
    assert response.json() == {
        "home_id": 1,
        "home_life": 18,
        "away_id": 2,
        "away_life": 0,
        "title": None,
        "description": None,
        "active": False,
        "id": 1,
        "home_user": {
            "email": "home@bar",
            "username": "home_team",
            "id": 1,
            "active": True
        },
        "away_user": {
            "email": "away@bar",
            "username": "away_team",
            "id": 2,
            "active": True
        }
    }

def test_delete_home_user():
    response = client.delete(f"/users/{context.get('home_id', 1)}")
    assert response.status_code == 200

def test_delete_away_user():
    response = client.delete(f"/users/{context.get('away_id', 2)}")
    assert response.status_code == 200
