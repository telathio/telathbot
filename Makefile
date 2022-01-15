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

pytest:
	export PYTHONPATH=${ROOT_DIR}:$$PYTHONPATH && \
	py.test tests

#-----------------------------------------------------------------------
# Run Rules
#-----------------------------------------------------------------------


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