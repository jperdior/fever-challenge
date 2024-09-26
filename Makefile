PWD = $(shell pwd)
PROJECT_NAME = fever-challenge
API=api
DOCKER_COMPOSE=docker-compose -p ${PROJECT_NAME} -f ${PWD}/ops/docker/docker-compose.yml
DOCKER_COMPOSE_FETCHER=docker-compose -p ${PROJECT_NAME} -f ${PWD}/ops/docker/docker-compose.fetcher.yml
GREEN=\033[0;32m
RESET=\033[0m

.EXPORT_ALL_VARIABLES:

# this is godly
# https://news.ycombinator.com/item?id=11939200
.PHONY: help
help:
ifeq ($(UNAME), Linux)
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
else
	@# this is not tested, but prepared in advance for you, Mac drivers
	@awk -F ':.*###' '$$0 ~ FS {printf "%15s%s\n", $$1 ":", $$2}' \
		$(MAKEFILE_LIST) | grep -v '@awk' | sort
endif

start: build run

build:
	@${DOCKER_COMPOSE} build

run:
	@${DOCKER_COMPOSE} up -d

stop:
	@${DOCKER_COMPOSE} down

restart: stop start

lint:
	@${DOCKER_COMPOSE} exec ${API} black src/

restart-fetcher: stop-fetcher start-fetcher

start-fetcher: build-fetcher run-fetcher

build-fetcher:
	@${DOCKER_COMPOSE_FETCHER} build

run-fetcher:
	@${DOCKER_COMPOSE_FETCHER} up -d

stop-fetcher:
	@${DOCKER_COMPOSE_FETCHER} down