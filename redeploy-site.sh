#!/bin/bash

# fetch the latest git repo
git fetch && git reset origin/main --hard

# stop and remove the existing containers
docker compose -f docker-compose.prod.yml down

# build and start the containers
docker compose -f docker-compose.prod.yml up -d --build