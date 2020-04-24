from flask import Flask

app = Flask(__name__)


@app.route('/mood', methods=["GET", "POST"])
def mood():
    return 'test'


if __name__ == '__main__':
    app.run()
