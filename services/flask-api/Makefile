# ----- CONFIGURATION -----
APP_NAME := flask-api
VERSION  := $(shell cat VERSION)
IMAGE_REPO ?= local
IMAGE_TAG := $(IMAGE_REPO)/$(APP_NAME):$(VERSION)
COMMIT_SHA := $(shell git rev-parse --short HEAD)
IMAGE_SHA_TAG := $(IMAGE_REPO)/$(APP_NAME):$(COMMIT_SHA)

# Allow overriding the docker command (e.g., DOCKER="sudo docker")
DOCKER ?= docker

.DEFAULT_GOAL := help

# ----- PHONY TARGETS -----
.PHONY: help build run stop logs shell version bump-patch bump-minor bump-major tag-latest push clean ci-build ci-smoke

# ----- HELP -----
help:
	@echo "Available targets:"
	@echo "  make build        Build image tagged with version and commit SHA"
	@echo "  make run          Run container (foreground, port 5000)"
	@echo "  make stop         Stop running container named $(APP_NAME)"
	@echo "  make logs         Tail logs of running container"
	@echo "  make shell        Start an interactive shell inside container"
	@echo "  make version      Show current version"
	@echo "  make bump-patch   Increment patch version"
	@echo "  make bump-minor   Increment minor version"
	@echo "  make bump-major   Increment major version"
	@echo "  make tag-latest   Tag built image also as :latest"
	@echo "  make push         Push version + commit + latest tags (set IMAGE_REPO first)"
	@echo "  make ci-build     (CI) Wrapper around build (future CI-specific flags)"
	@echo "  make ci-smoke     (CI) Run ephemeral container + health probe (port 5001)"
	@echo "  make clean        Remove local images for this app"

# ----- BUILD -----
build:
	@echo "Building version $(VERSION) (commit $(COMMIT_SHA))"
	$(DOCKER) build -t $(IMAGE_TAG) -t $(IMAGE_SHA_TAG) .

# ----- RUN / STOP / LOGS -----
run:
	$(DOCKER) run --rm --name $(APP_NAME) -p 5000:5000 $(IMAGE_TAG)

stop:
	- $(DOCKER) stop $(APP_NAME)

logs:
	$(DOCKER) logs -f $(APP_NAME)

shell:
	$(DOCKER) run --rm -it $(IMAGE_TAG) /bin/sh

# ----- VERSION MANAGEMENT -----
version:
	@echo "$(VERSION)"

bump-patch:
	./scripts/bump_version.sh patch

bump-minor:
	./scripts/bump_version.sh minor

bump-major:
	./scripts/bump_version.sh major

# ----- TAG MANAGEMENT -----
tag-latest:
	$(DOCKER) tag $(IMAGE_TAG) $(IMAGE_REPO)/$(APP_NAME):latest

# ----- PUSH (REGISTRY) -----
push:
	@if [ "$(IMAGE_REPO)" = "local" ]; then echo "Set IMAGE_REPO to your Docker Hub repo (e.g., username) before pushing"; exit 2; fi
	$(DOCKER) push $(IMAGE_TAG)
	$(DOCKER) push $(IMAGE_SHA_TAG)
	$(DOCKER) tag $(IMAGE_TAG) $(IMAGE_REPO)/$(APP_NAME):latest
	$(DOCKER) push $(IMAGE_REPO)/$(APP_NAME):latest
	@echo "Pushed: $(IMAGE_TAG), $(IMAGE_SHA_TAG), $(IMAGE_REPO)/$(APP_NAME):latest"

# ----- CI HELPERS -----
ci-build: build
	@echo "CI build complete (version: $(VERSION), commit: $(COMMIT_SHA))"

ci-smoke:
	@echo "Running CI smoke test..."
	@set -e; \
	VERSION=$$(cat VERSION); \
	CONTAINER=ci-$(APP_NAME)-smoke; \
	HEALTH_URL=http://127.0.0.1:5000/health; \
	echo "Starting container $$CONTAINER from image $(IMAGE_REPO)/$(APP_NAME):$$VERSION (no host port mapping)"; \
	$(DOCKER) rm -f $$CONTAINER >/dev/null 2>&1 || true; \
	$(DOCKER) run -d --name $$CONTAINER $(IMAGE_REPO)/$(APP_NAME):$$VERSION; \
	echo "Probing health endpoint inside container..."; \
	OK=0; \
	for i in $$(seq 1 15); do \
	  if $(DOCKER) exec $$CONTAINER python - <<'PY' >/dev/null 2>&1; then \
	      echo "Health check PASSED on attempt $$i"; OK=1; break; \
	  else \
	      echo "Attempt $$i failed; retrying..."; sleep 1; \
	  fi; \
	done; \
	if [ "$$OK" != "1" ]; then \
	  echo "Health check FAILED after retries. Showing logs:"; \
	  $(DOCKER) logs $$CONTAINER || true; \
	  $(DOCKER) rm -f $$CONTAINER >/dev/null 2>&1 || true; \
	  exit 1; \
	fi; \
	$(DOCKER) rm -f $$CONTAINER >/dev/null 2>&1 || true; \
	echo "Smoke test complete."

# ----- CLEAN -----
clean:
	- $(DOCKER) rmi $(IMAGE_TAG) 2>/dev/null || true
	- $(DOCKER) rmi $(IMAGE_SHA_TAG) 2>/dev/null || true
	- $(DOCKER) rmi $(IMAGE_REPO)/$(APP_NAME):latest 2>/dev/null || true
	@echo "Cleanup attempted."

