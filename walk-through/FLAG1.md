# Stage 1: Login per SQL Injection

## Ziel
Die Standard-Login-Seite erlaubt eine unsichere SQL-Abfrage. Nutze dies, um dich ohne gültiges Passwort einzuloggen und die erste Flag zu erhalten.

## Schritt-für-Schritt

1. Öffne die Login-Seite:  
http://localhost:80/login

python
Kopieren
Bearbeiten
2. Gib folgende Daten ein:  
- **Username**: `testuser' OR '1'='1`
- **Password**: beliebig (z. B. `foo`)

3. Nach erfolgreichem Login wird dir im Browser die Flag angezeigt:  

`FLAG{sql_injection_success}`

Viel Erfolg bei Stage!