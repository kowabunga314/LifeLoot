from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app.user.schema import User, UserRead
from app.user.test.content import test_user_create, test_user
import json


client = TestClient(app)

class TestContext():
    user = None
    access_token = None
    headers = None

context = TestContext()

def test_create_user():
    response = client.post('/users/signup', json.dumps(test_user_create.dict()))
    
    assert response.status_code == 200
    assert response.json()['username'] == test_user.username
    assert response.json()['email'] == test_user.email
    assert response.json()['active'] == test_user.active

    context.user = UserRead(**response.json())

def test_login_user():
    body = {'username': context.user.username, 'password': test_user_create.password}
    response = client.post('/token', body)
    assert response.status_code == 200
    context.access_token = response.json()['access_token']
    context.headers = {'Authorization': f"Bearer {context.access_token}"}

def test_get_user_by_id():
    response = client.get(f"/users/{context.user.id}", headers=context.headers)
    assert response.status_code == 404

def test_get_user_by_username():
    response = client.get(f"/users/{context.user.username}", headers=context.headers)

    assert response.status_code == 200
    assert response.json()['email'] == context.user.email
    assert response.json()['username'] == context.user.username
    assert response.json()['id'] == context.user.id
    assert response.json()['active'] == context.user.active

def test_get_user_by_email():
    response = client.get(f"/users/{context.user.email}", headers=context.headers)
    assert response.status_code == 404

def test_read_users():
    response = client.get("/users/", headers=context.headers)
    assert response.status_code == 200
    assert response.json() == [context.user.dict()]

def test_delete_user():
    response = client.delete(f"/users/{context.user.id}", headers=context.headers)
    assert response.status_code == 200
