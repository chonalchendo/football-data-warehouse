# Makefile

# The default goal
.DEFAULT_GOAL := help

# Default values
EXTRACT_SCRIPT ?= transfermarkt 

# Default arguments
ARGS = --crawler squads --season all


# Help target
help:
	@echo "Available commands:"
	@echo "  make run-transfermarkt-scraper  : Run the Transfermarkt scraper"
	@echo "  make help         : Show this help message"

# Target to run the transfermarkt scraper
run-transfermarkt-crawler:
	@echo "Running scraper..."
	src/run.sh $(EXTRACT_SCRIPT) $(ARGS)
