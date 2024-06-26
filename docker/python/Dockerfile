FROM python:3.12 as requirements-stage
ARG ENV

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN if [ "$ENV" = "DEV" ]; then \
    poetry export -f requirements.txt --output requirements.txt --without-hashes --dev; \
    else \
    poetry export -f requirements.txt --output requirements.txt --without-hashes; \
    fi

FROM python:3.12

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update -q && apt-get install -yq netcat-traditional

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --default-timeout=100 --upgrade -r /app/requirements.txt

COPY . .


RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["sh", "./scripts/start.sh"]
