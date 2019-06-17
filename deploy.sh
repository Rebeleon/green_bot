#!/bin/bash
# fail fast after any error in commands
set -e

git checkout master

eval $(docker-machine env core)

docker build -t hub.ferumflex.com/ferumflex/waterbot:prod . && docker push hub.ferumflex.com/ferumflex/waterbot:prod

docker stack deploy -c docker-swarm.yml waterbot --with-registry-auth --prune
