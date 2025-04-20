FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends openssh-server \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /var/run/sshd /home/admin/.ssh

RUN useradd -m -d /home/admin -s /bin/bash admin \
 && chmod 700 /home/admin/.ssh \
 && chown admin:admin /home/admin

COPY keys/admin_rsa.pub /home/admin/.ssh/authorized_keys
RUN chmod 600 /home/admin/.ssh/authorized_keys \
 && chown admin:admin /home/admin/.ssh/authorized_keys

RUN sed -i \
      -e 's/^#\?PasswordAuthentication .*/PasswordAuthentication no/' \
      -e 's/^#\?PubkeyAuthentication .*/PubkeyAuthentication yes/' \
      /etc/ssh/sshd_config

WORKDIR /app
ENV PYTHONPATH=/app/src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY backup.zip /opt/backup/backup.zip

EXPOSE 22 8000

CMD ["/bin/bash", "-lc", "\
    /usr/sbin/sshd -D & \
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src/api \
"]
