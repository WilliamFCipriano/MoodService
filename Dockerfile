FROM debian:latest
LABEL maintainer="Will Cipriano"
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip
COPY ./ ./app
WORKDIR ./app
RUN pip3 install -r requirements.txt
RUN python3 setup.py install
EXPOSE 5000
CMD python3 MoodService/app.py