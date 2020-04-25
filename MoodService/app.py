from flask import Flask
from flask import request
from flask import jsonify
import MoodService.repositories.sqlite_util as database_util
from sqlite3 import Error as sqliteError
from MoodService.services import user as user_service
from MoodService.services import session as session_service
from MoodService.exceptions.user import UserPasswordValidationException

app = Flask(__name__)


@app.route('/mood', methods=["GET", "POST"])
def mood():
    return 'test'


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
    app.run()


def init_db():
    database_util.remove_database()
    database_util.create_database_if_not_exists()