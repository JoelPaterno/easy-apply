import pytest
from easyapplyapp.db import *

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('easyapplyapp.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initalised the db' in result.output
    assert Recorder.called