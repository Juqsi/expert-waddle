# Stage 3: JWT-Token knacken

## Ziel
In Stage 2 wurde durch die Änderung nur das Frontend bearbeitet, bei Anfragen an das Backend ist man immer noch nicht Admin.
Das Frontend hält ein JWT im LocalStorage, signiert mit HMAC-SHA256. Knacke das Secret, um einen neuen Token mit `admin:true` zu erzeugen.

## Vorbereitung
- Eine Beispiel-Wordlist ist `rockyou.txt`.
- Ein Crack-Skript findest du im Walkthrough als `crack.py`.

## Schritt-für-Schritt

1. Lese dein aktuelles Token aus dem LocalStorage (F12 → Application → LocalStorage → `auth` → `token`).
2. Starte das Brute-Force-Skript:
 ```bash
 python3 crack.py \
   --token <dein_original_token> \
   --wordlist rockyou.txt \
   --new-payload '{"username":"testuser","admin":true}'
```
Das Skript gibt dir deinen Secret-Key zurück und liefert den geforgten JWT mit "admin":true.

Setze im LocalStorage den neuen Token mit den Entwickler Tool:

Lade die Seite neu und lade im Admin-Tab die `backup.zip` herunter. Dort findest du dann `FLAG{jwt_admin_token_forged}`.

Stage 3 gemeistert!