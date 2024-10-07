FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN pip install --no-cache -U pip
RUN pip install --no-cache poetry

RUN poetry config virtualenvs.create false

COPY ./pyproject.toml /app
COPY ./poetry.lock /app

RUN poetry install --no-interaction --no-root -vvv

RUN /bin/bash -c "poetry shell"

ADD . /app

RUN chmod +x /app/src/run.sh

CMD ["/bin/bash", "/app/src/run.sh"]
