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

# Install Google Cloud SDK
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH=$PATH:/root/google-cloud-sdk/bin

# Set up Git configuration (replace with your details)
RUN git config --global user.email "conalhenderson@gmail.com" && \
    git config --global user.name "Conal Henderson"

# # Set the Google Cloud credentials path
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

ADD . /app

# # set up dvc remote
# RUN dvc remote add -d myremote gs://football-data-warehouse/dvcstore

RUN chmod +x /app/src/run.sh

CMD ["/bin/bash"]


