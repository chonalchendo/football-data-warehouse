# Makefile

# The default goal
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available commands:"
	@echo "  make run-transfermarkt-scraper  : Run the Transfermarkt scraper"
	@echo "  make help         : Show this help message"

# Target to run the transfermarkt scraper
run-transfermarkt-scraper:
	@echo "Running scraper..."
	@./extractors/transfermarkt/run.sh
