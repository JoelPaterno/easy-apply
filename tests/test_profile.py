import pytest

def test_index(client, auth):
    auth.login
    assert client.get('/').status_code == 302

def test_extract_num 