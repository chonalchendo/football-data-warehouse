# Makefile

# The default goal
.DEFAULT_GOAL := help

# Default values
EXTRACT_SCRIPT ?= transfermarkt 

# Default arguments
ARGS = --crawler squads --season all

# Docker image name
DOCKER_IMAGE_NAME = football-data-warehouse


# Help target
help:
	@echo "Available commands:"
	@echo "  make run-transfermarkt-scraper  : Run the Transfermarkt scraper"
	@echo "  make help         : Show this help message"

# Target to run the transfermarkt scraper
local-transfermarkt-crawler:
	@echo "Running scraper..."
	src/run.sh $(EXTRACT_SCRIPT) $(ARGS)

local-version-transfermarkt:
	@echo "Versioning data..."
	src/version.sh $(EXTRACT_SCRIPT) 

# Target to build the docker image
docker-build:
	@echo "Building docker image..."
	docker build -t $(DOCKER_IMAGE_NAME) .

# Target to run the docker image with the transfermarkt pipeline
docker-transfermarkt-crawler:
	@echo "Running docker transfermarkt pipeline..."
	docker run -it \
    -v $(PWD)/data:/app/data \
		-v $(PWD)/.git:/app/.git \
		-v $(PWD)/.dvc:/app/.dvc \
		--env-file .env \
		$(DOCKER_IMAGE_NAME) /app/src/run.sh $(EXTRACT_SCRIPT) $(ARGS)

# Target to build and run the docker image
docker-pipeline: docker-build docker-transfermarkt-crawler




