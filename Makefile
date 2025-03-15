.PHONY: help build up down down-volumes logs restart

help:
	@echo "Available commands:"
	@echo "  make build        - Build Docker images using docker-compose."
	@echo "  make up           - Start containers in detached mode (background)."
	@echo "  make down         - Stop and remove containers (volumes are preserved)."
	@echo "  make down-volumes - Stop and remove containers and volumes (reinitializes the DB)."
	@echo "  make logs         - Show logs from the containers."
	@echo "  make restart      - Restart containers by removing volumes and starting them again."

# Build Docker images defined in docker-compose.yml
build:
	docker-compose build

# Start the containers in detached mode
up:
	docker-compose up -d

# Stop and remove containers without removing volumes
down:
	docker-compose down

# Stop and remove containers and volumes (useful for reinitializing the database and re-running SQL scripts)
down-volumes:
	docker-compose down -v

# Follow container logs in real-time
logs:
	docker-compose logs -f

# Restart containers: removes containers and volumes, then starts the services
restart: down-volumes up
