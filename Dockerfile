FROM python:3.7 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.7

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./alembic /code/alembic
COPY alembic.ini /code/alembic.ini

COPY ./cmd /code/cmd

RUN chmod +x /code/cmd/*.sh

CMD ["/bin/bash", "./cmd/docker-entrypoint.sh"]
