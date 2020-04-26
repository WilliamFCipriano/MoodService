from flask import Flask
from flask import request
from flask import jsonify
import MoodService.repositories.sqlite_util as database_util
from sqlite3 import Error as sqliteError
from MoodService.services import user as user_service
from MoodService.services import session as session_service
from MoodService.services import mood_report as mood_report_service
from MoodService.exceptions.user import UserPasswordValidationException
from MoodService.exceptions.session import SessionNotFoundException
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException

app = Flask(__name__)


@app.route('/mood', methods=["GET", "POST"])
def mood():

    if request.method == "POST":
        try:
            session = session_service.validate_token(request.form["token"])
        except SessionNotFoundException:
            return jsonify("You must login first to submit your mood"), 401

        try:
            mood_streak_total = mood_report_service.create_new_mood_report(session.user_int_id, request.form["mood"])
        except MoodAlreadySubmittedException:
            return jsonify("You have already submitted a mood today"), 403

        mood_streak_percentile = mood_report_service.get_streak_percentile(mood_streak_total)

        if mood_streak_percentile >= 50:
            return jsonify("Mood submitted successfully, you are in the %sth percentile of users!"
                           % mood_streak_percentile)
        else:
            return jsonify("Mood submitted successfully, see you again tomorrow!")


@app.route('/login', methods=["POST"])
def login():
    try:
        user = user_service.validate_user_password(request.form["username"], request.form["password"])
        session = session_service.create_session(user.int_id)
    except UserPasswordValidationException:
        return jsonify("Unable to validate credentials")
    return jsonify(session.__dict__)


@app.route('/register', methods=["POST"])
def register():
    try:
        user_service.register_new_user(request.form["username"], request.form["password"])
    except sqliteError:
        return jsonify("This username has already been reserved, please choose another.")
    return jsonify("User %s has been registered successfully" % request.form["username"])


if __name__ == '__main__':
    app.run(host='0.0.0.0')


def init_db():
    database_util.remove_database()
    database_util.create_database_if_not_exists()