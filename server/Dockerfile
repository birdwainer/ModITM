# nosemgrep:github.workflows.config.dockerfile-source-not-pinned
FROM python:3.11-slim
LABEL maintainer="Birdwainer <birdwainer@gmail.com>"

ENV PYTHONUNBUFFERED 1

COPY . /server
WORKDIR /server

ENV PATH="${PATH}:/root/.local/bin"
RUN apt-get update && apt-get install -y --no-install-recommends curl gcc git g++ libev-dev libyaml-dev tini && \
  curl -sSL https://install.python-poetry.org | python3 - && \
  poetry config virtualenvs.create false && \
  poetry install --no-root && \
  apt-get purge -y gcc g++ && apt -y autoremove --purge && rm -rf /var/cache/* /root/.cache/*

# nosemgrep:github.workflows.config.missing-user
CMD poetry run python server.py