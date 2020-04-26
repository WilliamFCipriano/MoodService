from flask import Blueprint
from flask import request
from flask import jsonify
from MoodService.exceptions.user import UsernameAlreadyInUseException

from MoodService.services import user as user_service

register = Blueprint('register', __name__)


@register.route('/register', methods=["POST"])
def post():
    try:
        user_service.register_new_user(request.form["username"], request.form["password"])
    except UsernameAlreadyInUseException:
        return jsonify("This username has already been reserved, please choose another.")
    return jsonify("User %s has been registered successfully" % request.form["username"])