from flask import Blueprint
from flask import jsonify
from flask import request
from MoodService.services import user as user_service
from MoodService.services import session as session_service
from MoodService.exceptions.user import UserPasswordValidationException

login = Blueprint('login', __name__)


@login.route('/login', methods=["POST"])
def post():
    """This endpoint returns a jsonified Session object when you provide it
    when a valid username and password"""
    try:
        user = user_service.validate_user_password(request.form["username"], request.form["password"])
    except UserPasswordValidationException:
        return jsonify("Unable to validate credentials")

    session = session_service.create_session(user.int_id)
    return jsonify(session.__dict__)
