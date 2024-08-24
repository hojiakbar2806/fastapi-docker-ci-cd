export $(shell cat .env | xargs)

.PHONY: up containers
docker-compose:
	@if [ "$(APP_IN_SERVER)" = "true" ]; then \
		sudo docker compose up -d; \
	else \
		docker compose up -d; \
	fi

.PHONY: ps
containers:
	@if [ "$(APP_IN_SERVER)" = "true" ]; then \
		sudo docker compose ps; \
	else \	
		docker compose ps; \
	fi