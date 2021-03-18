# Airflow 2.0 Fargate CDK

Deploy of Airflow using ECS Fargate and AWS CDK.

Uses Airflow image from [Bitnami](https://github.com/bitnami/bitnami-docker-airflow).

## Makefile

A comprehensive Makefile is available to execute common tasks. Run the following for help:

```
make help
```

###  Local Development
```
make airflow-local-up
```
Available on `0.0.0.0:8080`

Credentials are set with environment variables in `docker-compose.yml`
```
AIRFLOW_USERNAME: Airflow application username. Default: user
AIRFLOW_PASSWORD: Airflow application password. Default: Sionek123
AIRFLOW_EMAIL: Airflow application email. Default: user@example.com
```

To shut it down:
```
make airflow-local-down
```

## AWS CDK Development
If you wish to make changes to the infrastructure, you might need to have AWS CDK installed.  
Please follow the [AWS guide](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) to install it.