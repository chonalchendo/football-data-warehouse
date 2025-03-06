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
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make dagster-dev             : Run dagster dev server"
	@echo "  make dagster-asset-list      : List all dagster assets"
	@echo "  make dagster-run-asset       : Materialise a specific dagster asset"
	@echo "  make dagster-asset-partition : Materialise a specific dagster asset partition"
	@echo "  make dagster-job-partitions  : Run a specific dagster job with partitions"
	@echo "  make dbt-build               : Run pipeline for dbt assets"
	@echo "  make dbt-compile             : Compile dbt models"

.PHONY: check_format
check_format:
	@echo "Checking format of codebase..."
	uv run ruff check

.PHONY: format
format:
	@echo "Running formatter..."
	uv run ruff check --select I --fix . # sort imports
	uv run ruff format . # format files

.PHONY: check_types
check_types:
	@echo "Checking types..."
	uv run mypy foothouse/

.PHONY: sql_lint
sql_lint:
	@echo "Linting SQL files..."
	uv run sqlfluff lint dbt/models --dialect duckdb

.PHONY: sql_fix
sql_fix:
	@echo "Fixing SQL files..."
	uv run sqlfluff fix dbt/models --dialect duckdb


# Target to build the docker image
.PHONY: docker_build
docker_build:
	@echo "Building docker image..."
	docker build \
	--platform=$(PLATFORM) \
	--build-arg BRANCH=$(BRANCH) \
	-t $(DOCKER_IMAGE_NAME):$(IMAGE_TAG) .

.PHONY: docker_login_dockerhub
docker_login_dockerhub:
	@echo "Logging in to DockerHub with token"
	@echo ${DOCKER_TOKEN}	| docker login --username chonalchendo --password-stdin

.PHONY: docker_push_dockerhub
docker_push_dockerhub: docker_build docker_login_dockerhub
	@echo "Pushing docker image..."
	docker push $(DOCKER_IMAGE_NAME):$(IMAGE_TAG)

# # Target to run the docker image with the transfermarkt pipeline
# .PHONY: docker_transfermarkt_crawler
# docker_transfermarkt_crawler:
# 	docker run -it \
# 		-v $(PWD):/app \
# 		-v $(LOCAL_GCP_CREDS):$(DOCKER_GCP_CREDS) \
# 		--env-file .env \
# 		$(DOCKER_IMAGE_NAME) /app/src/run.sh $(EXTRACT_SCRIPT) $(TRANSFERMARKT_ARGS)

# # Target to build and run the docker image
# docker-pipeline: docker-build docker-transfermarkt-crawler

# # DVC pull data from gcp 
# # dvc_pull:
# # 	dvc remote modify --local gcs credentialpath $(LOCAL_GCP_CREDS)
# # 	dvc pull

.PHONY: dagster_dev
dagster_dev:
	uv run dagster dev -m foothouse.orchestrator

# dagster-asset-list:
# 	uv run dagster asset list -m orchestrator.orchestrator

# dagster-run-asset:
# 	uv run dagster asset materialize -m orchestrator.orchestrator --select $(ASSET)

# dagster-asset-partition:
# 	uv run dagster asset materialize -m orchestrator.orchestrator --select $(ASSET) --partition $(SEASON)

# dagster-job-partitions:
# 	uv run dagster job backfill -m orchestrator.orchestrator -j $(JOB) --partitions $(SEASON)

# dbt-build:
# 	cd dbt && dbt build

# dbt-compile:
# 	cd dbt && dbt compile

.PHONY: download_data
download_data:
	python3 src/downloaders/s3.py --folder staging --output ./data/public
	python3 src/downloaders/s3.py --folder curated --output ./data/public

.PHONY: create_data_schema
create_data_schema:
	python3 src/uploaders/generate_kaggle_schema.py

.PHONY: kaggle_create_dataset
kaggle_create_dataset:
	kaggle datasets create -p ./data/public/ --public

.PHONY: kaggle_update_dataaset
kaggle_update_dataaset:
	kaggle datasets version -p ./data/public/ -m 'Update data'

.PHONY: kaggle_upload
kaggle_upload: download_data create_data_schema kaggle_update_dataaset
kaggle_upload:
	rm -rf data/public/*.csv

	
