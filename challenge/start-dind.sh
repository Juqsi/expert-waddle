#!/bin/sh
set -eux

/usr/local/bin/dockerd-entrypoint.sh dockerd &

while [ ! -S /var/run/docker.sock ]; do sleep 0.1; done

cd /app/challenge
docker compose up -d

exec tail -f /dev/null
