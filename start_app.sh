#!/bin/bash -xe
# IMPORTANT: Make certain $USER is set on your system!

export DEFAULT_USER=${USER}
export WORKERS=4
export PORT=8002

export THELMA_SECRET_KEY=${THELMA_SECRET_KEY}

# Version Information
export MAJOR_VERSION=1
export MINOR_VERSION=3
export PATCH_LEVEL=0
export RELEASE=""



# TELEMETRY API Variables
export HTTP_PROTOCOL="http"
export TELEMETRY_API_HOST=${TELEMETRY_API_HOST}
export TELEMETRY_API_PORT=${TELEMETRY_API_PORT}

DJANGO_SETTINGS_MODULE=config.settings.base

sudo /usr/local/bin/docker-compose down && sudo /usr/local/bin/docker-compose build;

sudo /usr/local/bin/docker-compose up -d