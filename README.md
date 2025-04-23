# Pflanzen-Erkennungs-CTF Challenge

Willkommen zur CTF-Challenge rund um eine Pflanzen-Erkennungs-Webanwendung. Ziel ist es, Schritt für Schritt verschiedene Sicherheitslücken auszunutzen und insgesamt sechs Flags zu erlangen.

## Setup

1. Repository klonen und ins Hauptverzeichnis wechseln.
2. Environment-Variablen oder Secrets sind bereits in den Compose-Files hinterlegt.
3. Starte alles per:

   ```bash
   docker compose up --build
   ```

   Dieser Build- und Startvorgang kann ein paar Minuten dauern.

4. Nach erfolgreichem Start ist die Weboberfläche unter
   ```
   http://localhost:80
   ```
   erreichbar.

---

**Hinweis:** Diese README enthält nur die nötigen Informationen zum Setup und Ablauf, keine Lösungshinweise. Für jede Teilschritt gibt es eine eigene Stage-README mit den Details und der jeweiligen Flag.