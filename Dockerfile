FROM alpine

RUN apk add python3 py3-pip
RUN pip3 install flask

ENV FLASK_APP=app
