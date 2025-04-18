#!/bin/sh
set -e

# erzwinge, dass die Docker‑CLI den rootless Socket verwendet
export DOCKER_HOST=unix:///run/user/1001/docker.sock

 # A) Starte den rootless Docker‑Daemon
/usr/local/bin/dockerd-entrypoint.sh &


# 2) auf Bereit­schaft prüfen
until docker info > /dev/null 2>&1; do
  echo "⏱️ Warte auf Docker‑Daemon…"
  sleep 2
done
echo "🚀 Rootless Docker‑Daemon läuft"

# 3) Challenge‑Container starten
cd ./challenge
docker compose up -d

# 4) Base‑Container am Leben halten
tail -f /dev/null