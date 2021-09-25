# docker/backend/Dockerfile

FROM python:3.8.3-alpine

WORKDIR /app
ADD ./ /app


RUN pip install --upgrade pip
RUN pip install gunicorn

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN apk add musl-dev mariadb-dev gcc
RUN pip install mysqlclient

RUN pip install -r requirements.txt