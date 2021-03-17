# Airflow 2.0 Fargate CDK

Deploy of Airflow using ECS Fargate and AWS CDK.

Uses Airflow image from [Bitnami](https://github.com/bitnami/bitnami-docker-airflow).

## Makefile

A comprehensive Makefile is available to execute common tasks. Run the following for help:

```
make help
```

###  Run it locally
```
make run-airflow-local
```
Credentials are set with environment variables in `docker-compose.yml`
```
AIRFLOW_USERNAME: Airflow application username. Default: user
AIRFLOW_PASSWORD: Airflow application password. Default: Sionek123
AIRFLOW_EMAIL: Airflow application email. Default: user@example.com
```
To shut it down:
```
make kill-airflow-local
```

