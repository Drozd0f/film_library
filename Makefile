COMPOSE ?= docker-compose -f docker-compose.yml

run:
	$(COMPOSE) up --build -d
	@echo http://localhost:5000

rm:
	$(COMPOSE) rm -sfv

log-%:
	$(COMPOSE) logs -f $*

lint:
	@flake8
