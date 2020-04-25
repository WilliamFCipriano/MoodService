FROM python:3.7.1

WORKDIR /docker-flask

COPY . .

RUN ["pip3", "install", "pipenv"]

RUN ["pipenv", "install"]

CMD pipenv run python MoodService/app.py