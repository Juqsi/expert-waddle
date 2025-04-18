# challenge/Dockerfile
FROM docker:24.0.5-dind-rootless

USER root

# Installiere die UID‑Map‑Tools
RUN apk add --no-cache shadow-uidmap

# User/Group & Sub‑UID/Sub‑GID
RUN addgroup docker \
 && adduser -D -G docker docker \
 && echo "docker:100000:65536" >> /etc/subuid \
 && echo "docker:100000:65536" >> /etc/subgid

# HOME & Runtime-Verzeichnis
ENV HOME=/home/docker \
    XDG_RUNTIME_DIR=/run/user/1001

RUN mkdir -p $HOME/app \
 && mkdir -p $XDG_RUNTIME_DIR \
 && chown -R docker:docker $HOME \
 && chmod 700    $HOME \
 && chown docker:docker $XDG_RUNTIME_DIR \
 && chmod 700    $XDG_RUNTIME_DIR

USER docker
WORKDIR $HOME/app

EXPOSE 80 8000 22

COPY --chown=docker:docker . .
RUN chmod +x ./challenge/entrypoint.sh

ENTRYPOINT ["./challenge/entrypoint.sh"]
