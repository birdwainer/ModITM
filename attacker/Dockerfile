ROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install --no-install-recommends -yq \
    ufw \
    dsniff

ENTRYPOINT ["tail", "-f", "/dev/null"]