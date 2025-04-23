#!/bin/sh
set -eux

/usr/local/bin/dockerd-entrypoint.sh dockerd &

while [ ! -S /var/run/docker.sock ]; do sleep 0.1; done

cd /app/challenge
export DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)
docker compose up --build

exec tail -f /dev/null
