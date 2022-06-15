# use bash
SHELL=/bin/bash

# import dot env
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

rebuild: down build up

lint:
	@echo "Formatting source code"
	@pre-commit run --all-files

up:
ifdef profile
	docker-compose -f docker-compose.yml --profile $(profile) --env-file .env up -d
else
	docker-compose -f docker-compose.yml --env-file .env up -d
endif

down:
ifdef profile
	docker-compose -f docker-compose.yml --profile $(profile) --env-file .env down
else
	docker-compose -f docker-compose.yml --env-file .env down
endif
