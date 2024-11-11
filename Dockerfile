FROM python:3.12-slim 

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache -U pip && pip install --no-cache poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-root


# Set up Git configuration 
RUN git config --global user.email "football-data-warehouse-ci@football-data-warehouse.dev" && \
    git config --global user.name "CI Job" && \
    git config --global core.sshCommand "ssh -o StrictHostKeyChecking=no" 

ADD src/bootstrap.sh /app

ENTRYPOINT ["/bin/bash", "/app/bootstrap.sh"]

