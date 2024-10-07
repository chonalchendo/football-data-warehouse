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
run-transfermarkt-crawler:
	@echo "Running scraper..."
	src/run.sh $(EXTRACT_SCRIPT) $(ARGS)

version-transfermarkt-data:
	@echo "Versioning data..."
	src/version.sh $(EXTRACT_SCRIPT) 

# Target to build the docker image
docker-build:
	@echo "Building docker image..."
	docker build -t $(DOCKER_IMAGE_NAME) .

# Target to run the docker image
docker-run:
	@echo "Running docker image..."
	docker run -it $(DOCKER_IMAGE_NAME)

# Target to build and run the docker image
docker-pipeline: docker-build docker-run




