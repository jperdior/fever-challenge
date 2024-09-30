PWD = $(shell pwd)
PROJECT_NAME = fever-challenge
API=api
TEST=test
DOCKER_COMPOSE=docker-compose -p ${PROJECT_NAME} -f ${PWD}/ops/docker/docker-compose.yml
DOCKER_COMPOSE_ALL=docker-compose -p ${PROJECT_NAME} -f ${PWD}/ops/docker/docker-compose.yml -f ${PWD}/ops/docker/docker-compose.fetcher.yml
GREEN=\033[0;32m
RESET=\033[0m

.EXPORT_ALL_VARIABLES:

# this is godly
# https://news.ycombinator.com/item?id=11939200
.PHONY: help
help:
ifeq ($(UNAME), Linux)
	@grep -P '^[a-zA-Z_-]+:.*?### .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?### "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
else
	@# this is not tested, but prepared in advance for you, Mac drivers
	@awk -F ':.*####' '$$0 ~ FS {printf "%15s%s\n", $$1 ":", $$2}' \
		$(MAKEFILE_LIST) | grep -v '@awk' | sort
endif

start: build run ### Start the project

build: ### Build the project
	@${DOCKER_COMPOSE} build

run: ### Run the project
	@${DOCKER_COMPOSE} up -d

stop: ### Stop the project
	@${DOCKER_COMPOSE} down

restart: stop start

lint: ### Lint the project
	@${DOCKER_COMPOSE} exec ${API} black src/ tests/

mypy: ### Type check the project
	@${DOCKER_COMPOSE} exec ${API} mypy src/

restart-all: stop-all start-all ### Restart the all

start-all: build-all run-all ### Start the all

build-all: ### Build the all
	@${DOCKER_COMPOSE_ALL} build

run-all: ### Run the all
	@${DOCKER_COMPOSE_ALL} up -d

stop-all: ### Stop the all
	@${DOCKER_COMPOSE_ALL} down

logs: ### Show logs
	@${DOCKER_COMPOSE} logs -f

###@ Migration

init-migrations: ### Initialize the migrations
	@${DOCKER_COMPOSE} exec ${API} flask db init

migrate: ### Create a new migration
	@${DOCKER_COMPOSE} exec ${API} flask db migrate

upgrade: ### Upgrade the database
	@${DOCKER_COMPOSE} exec ${API} flask db upgrade

downgrade: ### Downgrade the database
	@${DOCKER_COMPOSE} exec ${API} flask db downgrade

###@ Tests

test:
	pytest

###@ Utils

docs:
	open http://localhost:5000/apidocs

fetch-events:
	@${DOCKER_COMPOSE} exec ${API} flask events fetch