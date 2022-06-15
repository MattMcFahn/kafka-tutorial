# use bash
SHELL=/bin/bash

# import dot env
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

rebuild: down build up

entry:
	# TODO: python entrypoint

setup: env pre_commit_install

env:
	@echo "Create virtual env and install dependencies"
	@poetry env use 3.9.5
	@poetry install

shell:
	@poetry shell

pre_commit_install:
	@echo "Install pre-commit"
	@poetry run pre-commit install

test: lint unit-test

lint:
	@echo "Formatting source code"
	@poetry run pre-commit run --all-files

unit-test:
	@echo "Running unit tests"
	@poetry run pytest --cov-report term-missing --cov=producer tests/

build:
	docker build -f Dockerfile -t producer .

up:
	docker-compose -f dev/docker-compose.yml --env-file .env up -d

down:
	docker-compose -f dev/docker-compose.yml --env-file .env down
