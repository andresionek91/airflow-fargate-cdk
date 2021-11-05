SHELL=/bin/bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: airflow-local-up
airflow-local-up: ## Runs airflow containers locally using docker-compose. Available on 0.0.0.0:8080. Usename: user, Password: Sionek123
	docker compose -f airflow/docker-compose.yml up -d

.PHONY: airflow-local-down
airflow-local-down: ## Kill all airflow containers created with docker-compose.
	docker compose -f airflow/docker-compose.yml down -v

.PHONY: init
init: dev-clean-local dev-install-local dev-test-local ## Clean environment and reinstall all dependencies

.PHONY: dev-clean-local
dev-clean-local: ## Removes project virtual env
	bash scripts/dev_clean_local.sh

.PHONY: dev-install-local
dev-install-local: ## Local install of the project and pre-commit using Poetry. Install AWS CDK package for development.
	npm install aws-cdk-local aws-cdk
	poetry install
	poetry run pre-commit install
	poetry run pip install -e infrastructure
	poetry run pip install -r airflow/airflow-requirements.txt
	ENTRYPOINT=-d poetry run localstack start --docker

.PHONY: dev-test-local
dev-test-local: ## Run local tests
	bash scripts/dev_test_local.sh

.PHONY: dev-deploy-local
dev-deploy-local: ## Deploy the infrastructure stack to localstack
	bash scripts/dev_deploy_local.sh