FROM python:3.11.6-alpine

WORKDIR /Message_Backend


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./message_client message_client/

COPY .env .
ENV $(cat .env | grep -v ^# | xargs)

WORKDIR /Message_Backend/message_client

EXPOSE 8000

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000"]

