-include .env

build:
	docker compose build

up:
	docker compose up -d

down:
	docker-compose down

log:
	docker compose logs

minecraft:
	docker exec -it $(MINECRAFT_CONTAINER_HOST) /bin/sh

discord:
	docker exec -it $(DISCORDBOT_CONTAINER_HOST) /bin/sh