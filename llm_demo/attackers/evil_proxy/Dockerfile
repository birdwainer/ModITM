FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install --no-install-recommends -yq \
    tcpdump \
    iptables \
    nginx \
    dsniff 

COPY startup.sh .

ENTRYPOINT ["./startup.sh"]