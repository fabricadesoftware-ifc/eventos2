FROM python:3.8-buster

RUN pip install poetry

COPY pyproject.toml poetry.lock manage.py /tmp/
RUN cd /tmp/ && poetry install --no-dev --no-root

COPY eventos2/ /tmp/eventos2/
COPY docker/production/backend.checks /tmp/eventos2/CHECKS

RUN cd /tmp/ && poetry install --no-dev
RUN cd /tmp/ && SECRET_KEY=static DATABASE_URL=sqlite:///:memory: poetry run python /tmp/manage.py collectstatic && chmod -R u=rwX,g=rX,o=rX /tmp/static

WORKDIR /tmp/eventos2
CMD poetry run gunicorn --worker-tmp-dir=/dev/shm --workers=2 --threads=4 --worker-class=gthread --bind=0.0.0.0:$PORT eventos2.wsgi
