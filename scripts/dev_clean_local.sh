#!/bin/bash
rm -rf .venv cdk.out */*/*.egg-info .pytest_cache
docker kill $(docker ps --filter name=airflow_ --quiet) || true
docker kill $(docker ps --filter name=localstack_main --quiet) || true