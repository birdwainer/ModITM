# nosemgrep:github.workflows.config.dockerfile-source-not-pinned
FROM python:3.11-slim
LABEL maintainer="Rashley <rashley@iqt.org>"

ENV PYTHONUNBUFFERED 1

COPY . /interceptor
WORKDIR /interceptor

ENV PATH="${PATH}:/root/.local/bin"
RUN apt-get update && apt-get install -y --no-install-recommends curl gcc git g++ libev-dev libyaml-dev tini \
ffmpeg libsm6 libxext6 && \
  curl -sSL https://install.python-poetry.org | python3 - && \
  poetry config virtualenvs.create false && \
  poetry install --no-root && \
  apt-get purge -y gcc g++ && apt -y autoremove --purge && rm -rf /var/cache/* /root/.cache/*

HEALTHCHECK CMD curl --fail http://localhost:5000/image/1 || exit 1

# nosemgrep:github.workflows.config.missing-user
CMD poetry run python interceptor.py