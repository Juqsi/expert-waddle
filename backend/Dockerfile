FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      openssh-server sudo bash unzip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd \
    && ssh-keygen -A

RUN useradd -m -s /bin/bash admin \
    && echo 'admin ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

COPY keys/admin_rsa.pub /home/admin/.ssh/authorized_keys

RUN chown -R admin:admin /home/admin/.ssh \
    && chmod 700 /home/admin/.ssh \
    && chmod 600 /home/admin/.ssh/authorized_keys

COPY backup.zip /opt/backup/backup.zip
RUN chmod 600 /opt/backup/backup.zip

RUN sed -i \
      -e 's/^#PasswordAuthentication yes/PasswordAuthentication no/' \
      -e 's/^#PubkeyAuthentication yes/PubkeyAuthentication yes/' \
      /etc/ssh/sshd_config

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 22 8000

CMD ["/bin/bash", "-lc", "\
    /usr/sbin/sshd && \
    uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src/api \
"]
