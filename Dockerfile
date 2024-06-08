FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

COPY .env.docker /app/.env
COPY . /app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python manage.py migrate \
    && python manage.py runserver 0.0.0.0:8000