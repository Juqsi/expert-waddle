# Stage 4: Backup herunterladen & SSH-Key finden

## Ziel
Auf der Admin-Seite kannst du nun eine `backup.zip` herunterladen. In dieser liegt ein SSH-Schlüssel.

## Schritt-für-Schritt

1. Klicke in der Admin-Oberfläche auf „Download Backup“.  
2. Speichere `backup.zip` lokal und entpacke sie:
3. Navigiere in das .ssh-Verzeichnis:

Dort findest du den Private-Key admin_rsa. 
Mit dem kannst du dich auf das Backend System schalten.

```shell
ssh -i ./admin_rsa -p 22 admin@localhost
```
**Hinweis**
Falls ein Fehler wege `WARNING: UNPROTECTED PRIVATE KEY FILE` kommt, müssen die rechte vorher noch angepasst werden `chmod 600 admin_rsa`.


Bei der begrüßung findest du `FLAG{ssh_key_buried_in_backup}`.
Gut gemacht, Stage 4 abgeschlossen!