COMPOSE ?= docker-compose -f docker-compose.yml

run: build
	$(COMPOSE) up -d
	@echo http://localhost:5000

build:
	$(COMPOSE) build

rm:
	$(COMPOSE) stop
	$(COMPOSE) rm -f

log-%:
	docker logs $* -f
