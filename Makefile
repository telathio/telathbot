SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = telathbot

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------
test: lint pytest specification-test

precommit: clean generate-requirements

build: clean build-package upload

build-local: clean build-package

#-----------------------------------------------------------------------
# Install
#-----------------------------------------------------------------------

install:
	pip install -U -r requirements.txt && \
	python setup.py install

#-----------------------------------------------------------------------
# Testing & Linting
#-----------------------------------------------------------------------
lint:
	pylint ${PROJECT_NAME} && \
	mypy ${PROJECT_NAME} --install-types --non-interactive;

pytest:
	export PYTHONPATH="${ROOT_DIR}:$$PYTHONPATH" && \
	py.test tests/unit_tests

tox:
	tox --parallel auto

#-----------------------------------------------------------------------
# Rules
#-----------------------------------------------------------------------
clean:
	rm -rf build; \
	rm -rf dist; \
	rm -rf UnleashClient.egg-info;

build-package:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*
