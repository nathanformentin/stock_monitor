FROM python:3

ENV PYTHONUNBUFFERED=2

WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8002" ]