#!/bin/bash -xe
# IMPORTANT: Make certain $USER is set on your system!

export DEFAULT_USER=${USER}
export WORKERS=4
export PORT=8002

export THELMA_SECRET_KEY=${THELMA_SECRET_KEY}

# Version Information
export MAJOR_VERSION=1
export MINOR_VERSION=1
export PATCH_LEVEL=0
export RELEASE=""


# TELEMETRY API Variables
export TELEMETRY_API_HOST=${TELEMETRY_API_HOST}
export TELEMETRY_API_PORT=${TELEMETRY_API_PORT}

DJANGO_SETTINGS_MODULE=config.settings.base

sudo docker-compose down && sudo docker-compose build;

sudo docker-compose up