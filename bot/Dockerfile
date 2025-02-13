FROM python:3.12

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false


WORKDIR /code
COPY pyproject.toml poetry.lock  /code/

RUN poetry install --no-root --no-interaction --no-ansi --no-cache

COPY  alembic.ini /code/

COPY migration /code/migration
COPY keys /code/keys
COPY src /code/src
COPY instruction /code/instruction
COPY .env /code

ENV PYTHONPATH="/code:"