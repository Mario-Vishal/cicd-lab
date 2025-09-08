APP_NAME := flask-api
VERSION := $(shell cat VERSION)
IMAGE_REPO ?= local
IMAGE_TAG := $(IMAGE_REPO)/$(APP_NAME):$(VERSION)
COMMIT_SHA := $(shell git rev-parse --short HEAD)
IMAGE_SHA_TAG := $(IMAGE_REPO)/$(APP_NAME):$(COMMIT_SHA)

.DEFAULT_GOAL := help

.PHONY: help build run stop logs shell version bump-patch bump-minor bump-major tag-latest push clean

help:
	@echo "Available targets:"
	@echo "  make build        Build image tagged with version and commit SHA"
	@echo "  make run          Run container (foreground)"
	@echo "  make stop         Stop running container named $(APP_NAME)"
	@echo "  make logs         Tail logs of running container"
	@echo "  make shell        Start an interactive shell inside container"
	@echo "  make version      Show current version"
	@echo "  make bump-patch   Increment patch version"
	@echo "  make bump-minor   Increment minor version"
	@echo "  make bump-major   Increment major version"
	@echo "  make tag-latest   Tag built image also as :latest"
	@echo "  make push         Push version + latest + commit tags (requires IMAGE_REPO != local)"
	@echo "  make clean        Remove local images for this app"

# ----- BUILD -----
build:
	@echo "Building version $(VERSION) (commit $(COMMIT_SHA))"
	sudo docker build -t $(IMAGE_TAG) -t $(IMAGE_SHA_TAG) .

# ----- RUN / STOP / LOGS -----
run:
	sudo docker run --rm --name $(APP_NAME) -p 5000:5000 $(IMAGE_TAG)

stop:
	sudo - docker stop $(APP_NAME)

logs:
	sudo docker logs -f $(APP_NAME)

shell:
	sudo docker run --rm -it $(IMAGE_TAG) /bin/sh

# ----- VERSION MANAGEMENT -----
version:
	@echo "$(VERSION)"

bump-patch:
	sudo ./scripts/bump_version.sh patch

bump-minor:
	sudo ./scripts/bump_version.sh minor

bump-major:
	sudo ./scripts/bump_version.sh major

# ----- TAG MANAGEMENT -----
tag-latest:
	sudo docker tag $(IMAGE_TAG) $(IMAGE_REPO)/$(APP_NAME):latest

# ----- PUSH (REGISTRY) -----
push:
	@if [ "$(IMAGE_REPO)" = "local" ]; then echo "Set IMAGE_REPO to your Docker Hub repo (e.g., username)"; exit 2; fi
	sudo docker push $(IMAGE_TAG)
	sudo docker push $(IMAGE_SHA_TAG)
	@docker tag $(IMAGE_TAG) $(IMAGE_REPO)/$(APP_NAME):latest
	sudo docker push $(IMAGE_REPO)/$(APP_NAME):latest
	@echo "Pushed: $(IMAGE_TAG), $(IMAGE_SHA_TAG), $(IMAGE_REPO)/$(APP_NAME):latest"

# ----- CLEAN -----
clean:
	- docker rmi $(IMAGE_TAG) 2>/dev/null || true
	- docker rmi $(IMAGE_SHA_TAG) 2>/dev/null || true
	- docker rmi $(IMAGE_REPO)/$(APP_NAME):latest 2>/dev/null || true
	@echo "Cleanup attempted."
