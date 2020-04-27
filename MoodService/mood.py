from flask import Blueprint
from flask import request
from flask import jsonify
from MoodService.services import mood_report as mood_report_service
from MoodService.services import session as session_service
from MoodService.exceptions.session import SessionNotFoundException
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException
from MoodService.exceptions.mood_report import NoPreviousMoodFoundException

mood = Blueprint('mood', __name__)


@mood.route('/mood', methods=["POST"])
def post():
    """This endpoint allows logged in users to submit a mood each day"""
    try:
        session = session_service.validate_token(request.form["token"])
    except SessionNotFoundException:
        return jsonify("You must login first to submit your mood."), 401

    try:
        mood_streak_total = mood_report_service.create_new_mood_report(session.user_int_id, request.form["mood"])
    except MoodAlreadySubmittedException:
        return jsonify("You have already submitted a mood today."), 403

    mood_streak_percentile = mood_report_service.get_streak_percentile(mood_streak_total)

    if mood_streak_percentile >= 50:
        return jsonify("Mood submitted successfully, you are in the %sth percentile of users!"
                       % mood_streak_percentile)
    else:
        return jsonify("Mood submitted successfully, see you again tomorrow!")


@mood.route('/mood', methods=["GET"])
def get():
    """This endpoint allows logged in users to retrieve previous moods"""
    try:
        session = session_service.validate_token(request.form["token"])
    except SessionNotFoundException:
        return jsonify("You must login first to look at your previous moods."), 401

    return jsonify(mood_report_service.get_mood_reports_by_id(session.user_int_id))


@mood.route('/mood', methods=["PATCH"])
def patch():
    """This endpoint allows the logged in user to modify a previously saved mood"""
    try:
        session = session_service.validate_token(request.form["token"])
    except SessionNotFoundException:
        return jsonify("You must login first to edit your mood."), 401

    try:
        mood_report_service.update_mood_report(session.user_int_id, request.form["mood"])
    except NoPreviousMoodFoundException:
        return jsonify("No previous mood found to edit, submit a new one!")

    return jsonify("Mood successfully edited.")
