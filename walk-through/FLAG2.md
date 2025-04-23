# Stage 2: Admin-Panel sichtbar machen

## Ziel
Nach Stage 1 bist du eingeloggt, hast aber kein Admin-Menü. Setze im LocalStorage das Feld, damit der Admin-Reiter erscheint.

## Schritt-für-Schritt

1. Öffne deine Browser-Entwicklertools (F12) → Reiter „Application“ bzw. „Speicher“.
2. Suche im LocalStorage das Item `auth`.
3. Dort ist eine JSON formatierter String mit dem feld `isAdmin`.
3. Ändere den Wert von `"false"` auf `"true"`.
4. Lade die Seite neu. Oben in der Navigationsleiste erscheint jetzt ein neuer „Admin“-Tab.

5. Klick auf „Admin“ – hier findest du deine zweite Flag:
`FLAG{admin_panel_unlocked}`

Glückwunsch, Stage 2 geschafft!  