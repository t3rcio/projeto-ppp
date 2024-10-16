# syntax=docker/dockerfile:1

FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y supervisor && apt-get install nano -y
RUN mkdir -p /var/log/supervisor

WORKDIR /code
COPY ./api-server/requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
COPY ./deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN chmod +x /code/deploy/start.sh
RUN /code/deploy/start.sh

RUN supervisord -c /etc/supervisor/conf.d/supervisord.conf &
