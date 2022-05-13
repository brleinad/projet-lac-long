FROM python:3.9.7-slim-buster
ENV LANG C.UTF-8

    # Keeps Python from generating .pyc files in the container
    # Turns off buffering for easier container logging
#ENV PYTHONFAULTHANDLER=1 \
#    PYTHONHASHSEED=random \
#    PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.6 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


RUN apt-get -y update && apt-get -y autoremove

RUN mkdir /app
WORKDIR /app

RUN apt-get install -y python python-pip python-dev curl netcat git \
  && apt-get clean \
  && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="${PATH}:/root/.poetry/bin"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . .

ENV ENV prod
ENV ALLOWED_HOSTS $ALLOWED_HOSTS

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
