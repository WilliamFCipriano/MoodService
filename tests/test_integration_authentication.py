import os
import tempfile
import pytest

from MoodService import app as MoonServiceFlask

@pytest.fixture
def client():
    db_fd, MoonServiceFlask.app.config['DATABASE'] = tempfile.mkstemp()
    MoonServiceFlask.app.config['TESTING'] = True

    with MoonServiceFlask.app.test_client() as client:
        with MoonServiceFlask.app.app_context():
            MoonServiceFlask.init_db()
        yield client

    os.close(db_fd)
    os.unlink(MoonServiceFlask.app.config['DATABASE'])


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def register(client, username, password):
    return client.post('/register', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def test_register(client):
    rv = register(client, "testUser1", "hunter2")
    assert b'registered successfully' in rv.data


def test_register_then_login(client):
    rv = register(client, "testUser2", "toomanysecrets")
    assert b'registered successfully' in rv.data

    rv = login(client, "testUser2", "toomanysecrets")
    assert b'"session_token"' in rv.data

