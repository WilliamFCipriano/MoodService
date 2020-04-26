from flask import Flask
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
    mood_report_service.calculate_mood_report_percentiles()


if __name__ == '__main__':
    update_percentiles()
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_percentiles, 'interval', minutes=15)
    scheduler.start()
    app.run(host='0.0.0.0')


def init_db():
    database_util.remove_database()
    database_util.create_database_if_not_exists()