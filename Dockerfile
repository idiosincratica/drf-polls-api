FROM python:3.8.6-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /django-drf-polls

COPY . .

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
