import os
import pytest
from easyapplyapp import create_app
from easyapplyapp.db import db_session
from easyapplyapp.models import User

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })

    #add test users to the db. 
    with app.app_context():
        #add data to test db using db_session
        user1 = User(name='test', password='pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', active=True)
        user2 = User(name='other', password='pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', active=True)
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()
    yield app

    #remove test users from the db.
    db_session.delete(user1)
    db_session.delete(user2)
    db_session.commit()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
