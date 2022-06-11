COMPOSE ?= docker-compose -f docker-compose.base.yml
COMPOSE_DEV ?= $(COMPOSE) -f docker-compose.dev.yml -p film_library-dev
COMPOSE_TEST ?= $(COMPOSE) -f docker-compose.test.yml -p film_library-test

run:
	$(COMPOSE_DEV) up --build -d
	@echo http://localhost:5000

rm:
	$(COMPOSE_DEV) rm -sfv

log-%:
	$(COMPOSE_DEV) logs -f $*

lint:
	@flake8


setup-testenv:
	docker run --name test-db \
	-e POSTGRES_USER=test \
	-e POSTGRES_PASSWORD=test \
	-e POSTGRES_DB=test \
	-p 5433:5432 \
	-d \
	postgres:latest


cleanup-testenv:
	docker rm -f test-db


test:
	$(COMPOSE_TEST) up --build --abort-on-container-exit
	$(COMPOSE_TEST) rm -fv
