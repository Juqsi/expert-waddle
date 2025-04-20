FROM python:3.11-slim

# 1) SSH-Server installieren und Verzeichnisse anlegen
RUN apt-get update \
 && apt-get install -y --no-install-recommends openssh-server \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /var/run/sshd /home/admin/.ssh

# 2) admin-User anlegen
RUN useradd -m -d /home/admin -s /bin/bash admin \
 && chmod 700 /home/admin/.ssh \
 && chown admin:admin /home/admin

# 3) Deinen Public Key kopieren und Rechte setzen
COPY keys/admin_rsa.pub /home/admin/.ssh/authorized_keys
RUN chmod 600 /home/admin/.ssh/authorized_keys \
 && chown admin:admin /home/admin/.ssh/authorized_keys

# 4) SSH konfigurieren: Passwort‑Login aus, Pubkey‑Login an
RUN sed -i \
      -e 's/^#\?PasswordAuthentication .*/PasswordAuthentication no/' \
      -e 's/^#\?PubkeyAuthentication .*/PubkeyAuthentication yes/' \
      /etc/ssh/sshd_config

WORKDIR /app
ENV PYTHONPATH=/app/src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6) App‑Code und Backup
COPY . .
COPY backup.zip /opt/backup/backup.zip

# 7) Ports freigeben
EXPOSE 22 8000

# 8) SSH‑Dämon starten und gleichzeitig UVicorn laufen lassen
CMD ["/bin/bash", "-lc", "\
    /usr/sbin/sshd -D & \
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src/api \
"]
