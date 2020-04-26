import os
import tempfile
from datetime import datetime, timedelta
import pytest
from MoodService.repositories import user as user_repository
from MoodService.repositories import mood_report as mood_report_repository
from MoodService.services import mood_report as mood_report_service
from MoodService import app as MoodServiceFlask


@pytest.fixture
def client():
    db_fd, MoodServiceFlask.app.config['DATABASE'] = tempfile.mkstemp()
    MoodServiceFlask.app.config['TESTING'] = True

    with MoodServiceFlask.app.test_client() as client:
        with MoodServiceFlask.app.app_context():
            MoodServiceFlask.init_db()
        yield client

    os.close(db_fd)
    os.unlink(MoodServiceFlask.app.config['DATABASE'])


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


def test_percentile_reporting(client):
    tired_user_id = user_repository.create_new_user("tiredUser", "hunter2")
    mood_report_repository.historical_mood_report(tired_user_id, "tired", datetime.now().date() - timedelta(days=5))
    mood_report_repository.historical_mood_report(tired_user_id, "really tired", datetime.now().date() - timedelta(days=4))
    mood_report_repository.historical_mood_report(tired_user_id, "tired", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(tired_user_id, "tired", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(tired_user_id, "tired", datetime.now().date() - timedelta(days=1))
    mood_report_service.create_new_mood_report(tired_user_id, "tired")

    sad_user_id = user_repository.create_new_user("realSadUser", "hunter3")
    mood_report_repository.historical_mood_report(tired_user_id, "really sad", datetime.now().date() - timedelta(days=4))
    mood_report_repository.historical_mood_report(tired_user_id, "sad", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(tired_user_id, "sad", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(tired_user_id, "sad", datetime.now().date() - timedelta(days=1))
    mood_report_service.create_new_mood_report(sad_user_id, "sad")

    mood_report_service.calculate_mood_report_percentiles()

    register(client, "percentileTestUser", "hunter4")
    user = user_repository.get_user_by_id("percentileTestUser")
    mood_report_repository.historical_mood_report(user.int_id, "happy", datetime.now().date() - timedelta(days=6))
    mood_report_repository.historical_mood_report(user.int_id, "sad", datetime.now().date() - timedelta(days=5))
    mood_report_repository.historical_mood_report(user.int_id, "angry", datetime.now().date() - timedelta(days=4))
    mood_report_repository.historical_mood_report(user.int_id, "sad", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(user.int_id, "happy", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(user.int_id, "sad", datetime.now().date() - timedelta(days=1))

    session_token = login(client, "percentileTestUser", "hunter4").json["session_token"]
    result = submit_mood(client, session_token, "great")
    print(result)
