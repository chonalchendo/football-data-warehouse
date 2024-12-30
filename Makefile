# Makefile
.DEFAULT_GOAL := help

# Default values
EXTRACT_SCRIPT ?= transfermarkt 
TRANSFERMARKT_ARGS = --crawler squads --season 2024
DOCKER_IMAGE_NAME = chonalchendo/football-data-warehouse
PLATFORM ?= linux/amd64
PLATFORM_TAG ?= linux-amd64
BRANCH ?= master
IMAGE_TAG = $(PLATFORM_TAG)-$(BRANCH)

# Help target
help:
	@echo "Available commands:"
	@echo "  make dagster-dev             : Run dagster dev server"
	@echo "  make dagster-run-asset       : Materialise a specific dagster asset"
	@echo "  make dagster-asset-partition : Materialise a specific dagster asset partition"
	@echo "  make dagster-job-partitions  : Run a specific dagster job with partitions"
	@echo "  make dbt-build               : Run pipeline for dbt assets"
	@echo "  make dbt-compile             : Compile dbt models"


format:
	@echo "Running formatter"
	black .
	isort .

# Target to build the docker image
docker-build:
	@echo "Building docker image..."
	docker build \
	--platform=$(PLATFORM) \
	--build-arg BRANCH=$(BRANCH) \
	-t $(DOCKER_IMAGE_NAME):$(IMAGE_TAG) .

docker-login-dockerhub:
	@echo "Logging in to DockerHub with token"
	@echo ${DOCKER_TOKEN}	| docker login --username chonalchendo --password-stdin

docker-push-dockerhub: docker-build docker-login-dockerhub
	@echo "Pushing docker image..."
	docker push $(DOCKER_IMAGE_NAME):$(IMAGE_TAG)

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
# dvc_pull:
# 	dvc remote modify --local gcs credentialpath $(LOCAL_GCP_CREDS)
# 	dvc pull

dagster-dev:
	uv run dagster dev -m orchestrator.orchestrator

dagster-run-asset:
	uv run dagster asset materialize -m orchestrator.orchestrator --select $(ASSET)

dagster-asset-partition:
	uv run dagster asset materialize -m orchestrator.orchestrator --select $(ASSET) --partition $(SEASON)

dagster-job-partitions:
	uv run dagster job backfill -m orchestrator.orchestrator -j $(JOB) --partitions $(SEASON)

dbt-build:
	cd dbt && dbt build

dbt-compile:
	cd dbt && dbt compile

download-data:
	python3 src/downloaders/s3.py --folder staging --output ./data/public
	python3 src/downloaders/s3.py --folder curated --output ./data/public

create-data-schema:
	python3 src/uploaders/generate_kaggle_schema.py

kaggle-create-dataset:
	kaggle datasets create -p ./data/public/ --public

kaggle-update-dataaset:
	kaggle datasets version -p ./data/public/ -m 'Update data'

kaggle-upload: download-data create-data-schema kaggle-update-dataaset
kaggle-upload:
	rm -rf data/public/*.csv

	
