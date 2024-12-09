FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

# Set up Git configuration 
RUN git config --global user.email "football-data-warehouse-ci@football-data-warehouse.dev" && \
    git config --global user.name "CI Job" && \
    git config --global core.sshCommand "ssh -o StrictHostKeyChecking=no" 

ADD src/bootstrap.sh /app
    
# Allow branch to be passed as a build argument with a default
ARG BRANCH=master
ENV BRANCH=$BRANCH

ENTRYPOINT ["/bin/bash", "/app/bootstrap.sh", "${BRANCH}"]


    