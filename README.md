# telathbot

[![CI](https://github.com/telathio/telathbot/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/telathio/telathbot/actions/workflows/ci.yml) [![Coverage Status](https://coveralls.io/repos/github/telathio/telathbot/badge.svg?branch=main)](https://coveralls.io/github/telathio/telathbot?branch=main)

A Discord/Xenforo bot!

## Pre-requisites
* [pyenv](https://github.com/pyenv/pyenv) (via [installer](https://github.com/pyenv/pyenv-installer))
* [poetry](https://python-poetry.org/docs/)
* Docker (with Go version of docker compose enabled)

## Local development
1. Create a `.env` file from `.env-local` that contains relevant variables.  (Mainly this will be the Discord webhook for testign.)
2. Run `poetry install` to create virtualenv and install dependencies.
3. Run `make local-dev-up` to start mock Xenforo database and MongoDB.  This can be used when testing.
4. Run `make test` to get fresh environments, run linters and tests.


