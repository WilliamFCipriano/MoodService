from flask import Flask
from flask import request
from MoodService.services import user as user_service

app = Flask(__name__)


@app.route('/mood', methods=["GET", "POST"])
def mood():
    return 'test'

@app.route('/login', methods=["POST"])
def login():
    if user_service.validate_user_password(
            request.form["username"], request.form["password"]):
        pass




if __name__ == '__main__':
    app.run()
