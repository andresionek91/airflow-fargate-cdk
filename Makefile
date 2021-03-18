SHELL=/bin/bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: airflow-local-up
airflow-local-up: ## Runs airflow containers locally using docker-compose. Available on 0.0.0.0:8080. Usename: user, Password: Sionek123
	docker-compose up -d

.PHONY: airflow-local-down
airflow-local-down: ## Kill all airflow containers created with docker-compose.
	docker-compose down -v

.PHONY: build-local
build-local: clean-local install-local test-local ## Clean environment and reinstall all dependencies

.PHONY: clean-local
clean-local: ## Removes project virtual env
	rm -rf .venv

.PHONY: install-local
install-local: ## Local install of the project and pre-commit using Poetry
	poetry install
	poetry run pre-commit install
	poetry run pip install -e infrastructure

.PHONY: test-local
test-local: ## Run local tests
	PYTHONPATH=src poetry run pytest