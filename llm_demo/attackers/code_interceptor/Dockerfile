# nosemgrep:github.workflows.config.dockerfile-source-not-pinned
FROM python:3.11-slim
LABEL maintainer="Rashley <rashley@iqt.org>"

ENV PYTHONUNBUFFERED 1

COPY . /code_interceptor
WORKDIR /code_interceptor

ENV PATH="${PATH}:/root/.local/bin"
RUN apt-get update && apt-get install -y --no-install-recommends curl \ 
  tcpdump \
  iptables \
  dsniff && \
  curl -sSL https://install.python-poetry.org | python3 - && \
  poetry config virtualenvs.create false && \
  poetry install --no-root && \
  apt-get purge -y gcc g++ && apt -y autoremove --purge && rm -rf /var/cache/* /root/.cache/*

HEALTHCHECK CMD curl -v --fail http://localhost:11434/health || exit 1

# nosemgrep:github.workflows.config.missing-user
ENTRYPOINT ["./startup.sh"]