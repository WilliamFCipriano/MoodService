from flask import Flask, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
import MoodService.repositories.sqlite_util as database_util
from MoodService.services import mood_report as mood_report_service
from MoodService.mood import mood
from MoodService.login import login
from MoodService.register import register

app = Flask(__name__)

app.register_blueprint(mood)
app.register_blueprint(login)
app.register_blueprint(register)


def update_percentiles():
    """Updates the precalculated percentiles and stores them
    in the database, runs every 15 minutes"""
    mood_report_service.calculate_mood_report_percentiles()


@app.route("/")
def root():
    return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_percentiles, 'interval', hours=1)
    scheduler.start()
    app.run(host='0.0.0.0')


def init_db():
    database_util.remove_database()
    database_util.create_database_if_not_exists()