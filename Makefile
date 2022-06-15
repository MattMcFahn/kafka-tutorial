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
	docker-compose -f docker-compose.yml --env-file .env up -d

down:
	docker-compose -f docker-compose.yml --env-file .env down
