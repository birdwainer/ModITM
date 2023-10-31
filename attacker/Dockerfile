FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install --no-install-recommends -yq \
    ufw \
    nginx \
    dsniff

COPY ufw /etc/default/ufw
COPY before.rules /etc/ufw/before.rules
RUN sysctl -w net.ipv4.ip_forward=1

ENTRYPOINT ["tail", "-f", "/dev/null"]