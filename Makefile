SHELL=/bin/bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Shows this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: run-airflow-local
run-airflow-local: ## Runs airflow containers locally using docker-compose. Available on 0.0.0.0:8080. Usename: user, Password: Sionek123
	docker-compose up -d

.PHONY: kill-airflow-local
kill-airflow-local: ## Kill all airflow containers created with docker-compose.
	docker-compose down -v