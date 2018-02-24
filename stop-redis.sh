#!/bin/bash

# this assumes docker is running and docker-compose is installed

echo "Stopping redis"
cd docker
docker-compose -f redis.yml stop
docker stop celredis1
docker rm celredis1

exit 0
