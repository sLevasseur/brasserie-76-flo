FROM python:3.8.0-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY . .

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python3 ./bakpak_project/manage.py collectstatic --noinput

RUN python3 ./bakpak_project/manage.py makemigrations

RUN python3 ./bakpak_project/manage.py migrate

EXPOSE 8000

CMD ["python3", "./bakpak_project/manage.py", "runserver", "0.0.0.0:8000"]
