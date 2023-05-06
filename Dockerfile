FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY env.template /code/.env

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /code/
