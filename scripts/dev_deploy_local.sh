#!/bin/bash
docker kill $(docker ps --filter name=localstack --quiet) || true
ENTRYPOINT=-d localstack start --docker
export AWS_ENDPOINT=http://localhost:4566
export DEPLOY_ENV=test
cdklocal bootstrap
cdklocal deploy "*" --verbose --require-approval never
exit 0