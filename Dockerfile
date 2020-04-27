FROM debian:latest
LABEL maintainer="Will Cipriano"
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip
COPY ./ ./app
COPY ./etc/databases/populated.db ./app/moodService.db
WORKDIR ./app
RUN pip3 install .
EXPOSE 5000
CMD python3 MoodService/app.py