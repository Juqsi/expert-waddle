FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
       openssh-server bash curl \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /var/run/sshd

ARG DOCKER_GID
RUN groupadd -g ${DOCKER_GID} docker \
 && useradd -m -d /home/admin -s /bin/bash -G docker admin \
 && usermod -U admin

RUN mkdir -p /home/admin/.ssh \
 && chown admin:admin /home/admin/.ssh \
 && chmod 700 /home/admin/.ssh

COPY keys/admin_rsa.pub /home/admin/.ssh/authorized_keys
RUN chown admin:admin /home/admin/.ssh/authorized_keys \
 && chmod 600 /home/admin/.ssh/authorized_keys

RUN sed -i \
      -e 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' \
      -e 's/^#\?ChallengeResponseAuthentication.*/ChallengeResponseAuthentication no/' \
      /etc/ssh/sshd_config \
 && echo 'MaxAuthTries 50' >> /etc/ssh/sshd_config \
 && ssh-keygen -A

COPY ssh_banner.txt /etc/ssh/ssh_banner.txt

RUN echo 'Banner /etc/ssh/ssh_banner.txt' >> /etc/ssh/sshd_config \
 && sed -i 's/^#\?Banner.*/Banner \/etc\/ssh\/ssh_banner.txt/' /etc/ssh/sshd_config


WORKDIR /app
ENV PYTHONPATH=/app/src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 22 8000

CMD ["/bin/bash","-lc", "\
    /usr/sbin/sshd -D -e -o LogLevel=VERBOSE & \
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir src/api \
"]
