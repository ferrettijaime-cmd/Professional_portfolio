#!/bin/bash

airflow db migrate

airflow users create \
  --username "$_AIRFLOW_WWW_USER_USERNAME" \
  --password "$_AIRFLOW_WWW_USER_PASSWORD" \
  --firstname "$AIRFLOW_FIRSTNAME" \
  --lastname "$AIRFLOW_LASTNAME" \
  --role Admin \
  --email "$AIRFLOW_EMAIL"