SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = telathbot

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------
test: lint pytest

build: clean build-package upload

#-----------------------------------------------------------------------
# Testing & Linting
#-----------------------------------------------------------------------

lint:
	export PYTHONPATH=${ROOT_DIR}:$$PYTHONPATH;
	mypy --install-types --non-interactive ${PROJECT_NAME};
	pylint ${PROJECT_NAME};
	black telathbot tests --target-version py310;

pytest:
	export PYTHONPATH=${ROOT_DIR}:$$PYTHONPATH && \
	CONTROL_LEVEL=test py.test tests

local-dev-up:
	docker compose -f tests/local_dev/docker-compose.yaml up -d

local-dev-down:
	docker compose -f tests/local_dev/docker-compose.yaml down

#-----------------------------------------------------------------------
# Run Rules
#-----------------------------------------------------------------------

run:
	uvicorn telathbot:app --reload --host 0.0.0.0

# Run in Docker
run-docker:
	docker run -it --rm --name ${PROJECT_NAME} \
	${PROJECT_NAME}:latest

#-----------------------------------------------------------------------
# Docker Rules
#-----------------------------------------------------------------------
# Build Docker image
docker:
	docker build -t ${PROJECT_NAME} .

# Deletes Docker image
clean-docker:
	docker rm ${PROJECT_NAME}
