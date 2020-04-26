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


def submit_mood(client, token, mood):
    return client.post('/mood', data=dict(
        token=token,
        mood=mood
    ), follow_redirects=True)


def test_mood_submission(client):
    register(client, "happyuser", "hunter2")
    session_token = login(client, "happyuser", "hunter2").json["session_token"]
    submit_mood(client, session_token, "happy")


def test_mood_submission_twice(client):
    register(client, "saduser", "hunter3")
    session_token = login(client, "saduser", "hunter3").json["session_token"]
    submit_mood(client, session_token, "sad")
    result = submit_mood(client, session_token, "sadder")

    assert result.status == "403 FORBIDDEN"
    assert result.json == 'You have already submitted a mood today'
