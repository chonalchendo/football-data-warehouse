# Makefile
.DEFAULT_GOAL := help

# Load environment variables
include .env
export

# Default values
EXTRACT_SCRIPT ?= transfermarkt 
TRANSFERMARKT_ARGS = --crawler squads --season 2024
DOCKER_IMAGE_NAME = football-data-warehouse

# Help target
help:
	@echo "Available commands:"
	@echo "  make run-transfermarkt-scraper  : Run the Transfermarkt scraper"
	@echo "  make docker-pipeline            : Build Docker image and run pipeline"
	@echo "  make help                       : Show this help message"

# Target to run the transfermarkt scraper locally
local-transfermarkt-crawler:
	@echo "Running scraper..."
	src/run.sh $(EXTRACT_SCRIPT) $(TRANSFERMARKT_ARGS)

local-version-transfermarkt:
	@echo "Versioning data..."
	src/version.sh $(EXTRACT_SCRIPT) 

# Target to build the docker image
docker-build:
	@echo "Building docker image..."
	docker build -t $(DOCKER_IMAGE_NAME) .

# Target to run the docker image with the transfermarkt pipeline
docker-transfermarkt-crawler:
	docker run -it \
		-v $(PWD):/app \
    -v $(LOCAL_GCP_CREDS):$(DOCKER_GCP_CREDS) \
    --env-file .env \
    $(DOCKER_IMAGE_NAME) /app/src/run.sh $(EXTRACT_SCRIPT) $(TRANSFERMARKT_ARGS)

# Target to build and run the docker image
docker-pipeline: docker-build docker-transfermarkt-crawler

# DVC pull data from gcp 
dvc_pull:
	dvc remote modify --local gcs credentialpath $(LOCAL_GCP_CREDS)
	dvc pull

local-dagster-pipeline:
	chmod +x orchestrator/scripts/run_local.sh
	orchestrator/scripts/run_local.sh

local-dagster-dev:
	dagster dev -m orchestrator.orchestrator

local-run-dagster-dbt:
	poetry run dagster job execute -m orchestrator.orchestrator --config orchestrator/config.yaml    

local-run-dagster-dbt-asset:
	poetry run dagster job execute -m orchestrator.orchestrator.assets.fbref.player_defense --config orchestrator/config.yaml

dbt-build:
	cd dbt_pipeline && dbt build

dbt-compile:
	cd dbt_pipeline && dbt compile
