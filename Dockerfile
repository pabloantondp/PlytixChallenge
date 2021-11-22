FROM python:3.8

RUN mkdir /plytix_app
WORKDIR /plytix_app

COPY Pipfile ./
COPY .env ./plytix_app
COPY flaskr/ /plytix_app/flaskr/

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --skip-lock


EXPOSE ${FLASK_PORT}

CMD flask run --port=${FLASK_PORT} --host='0.0.0.0'
