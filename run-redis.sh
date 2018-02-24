#!/bin/bash

# this assumes docker is running and docker-compose is installed

echo "Starting redis"
cd docker
docker-compose -f redis.yml up -d

exit 0
