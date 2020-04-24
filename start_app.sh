#!/bin/bash -xe
# IMPORTANT: Make certain $USER is set on your system!

docker-compose down && docker-compose build;

docker-compose up