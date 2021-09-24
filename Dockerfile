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



RUN adduser -D dockuser
RUN chown dockuser:dockuser -R /app/
RUN chmod -R +x /app
RUN chmod +x /app/wsgi-entrypoint.sh


RUN mkdir -p /app/django_static/
RUN chown dockuser:dockuser /app/django_static/
RUN mkdir -p /app/media
RUN chown dockuser:dockuser /app/media

USER dockuser
