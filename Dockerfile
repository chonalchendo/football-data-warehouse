FROM python:3.12-slim-bookworm


# create dagster_home directory
# RUN mkdir -p dagster_home
# ENV DAGSTER_HOME=/dagster_home
# ENV DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1

# COPY orchestrator/dagster.yaml ${DAGSTER_HOME}/dagster.yaml
# root path for dagster.yaml file
# ENV ROOT_PATH=${DAGSTER_HOME} 

WORKDIR /app
# ENV ROOT_PATH=/app/football-data-warehouse/football-data-warehouse

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache -U pip && pip install --no-cache poetry

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/




COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"
# RUN poetry config virtualenvs.create false \
#     && poetry install --no-dev --no-interaction --no-root


# Set up Git configuration 
RUN git config --global user.email "football-data-warehouse-ci@football-data-warehouse.dev" && \
    git config --global user.name "CI Job" && \
    git config --global core.sshCommand "ssh -o StrictHostKeyChecking=no" 

ADD src/bootstrap.sh /app
    
# Allow branch to be passed as a build argument with a default
ARG BRANCH=master
ENV BRANCH=$BRANCH

ENTRYPOINT ["/bin/bash", "/app/bootstrap.sh", "${BRANCH}"]


    