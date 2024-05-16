FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV PYTHONUNBUFFERED=1