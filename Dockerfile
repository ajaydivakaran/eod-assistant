FROM python:3.3.6-alpine

MAINTAINER Ajay Divakaran <ajay.divakaran86@hotmail.com>

ENV APP_HOME=/app

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY . $APP_HOME

# Install dependencies
RUN apk update && apk add build-base postgresql-dev
RUN pip install -r requirements.txt

EXPOSE 80
ENTRYPOINT ["/app/docker-entrypoint.sh"]

