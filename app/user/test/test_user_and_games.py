from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
import json


client = TestClient(app)