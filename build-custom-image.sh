#!/bin/bash

# Function to build all images
build_images() {
    docker build --rm -t airflow-custom:v1.1 -f services/airflow/Dockerfile services/airflow
    docker build --rm -t spark-custom:latest -f services/spark/Dockerfile services/spark
    docker build --rm -t superset_custom:v1.1 -f services/superset/Dockerfile services/superset
}

# Check for the "build-all" command
if [[ "$1" == "build-all" ]]; then
    build_images
else
    echo "Usage: $0 build-all"
    exit 1
fi