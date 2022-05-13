FROM python:3.9.5-slim-buster

RUN mkdir -p /usr/src/api
WORKDIR /usr/src/api

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="Trisoft <code@trisoft.co.in>"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
