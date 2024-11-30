import pytest
from flask import session
from easyapplyapp.db import db_session
from easyapplyapp.models import User

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register', data={'username': 'ab', 'password': 'a'})
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        user = User.query.filter(User.name == 'ab').first()
        assert user is not None

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        user = User.query.filter(User.name == 'test').first()
        assert session['user_id'] == user.id
        

def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session