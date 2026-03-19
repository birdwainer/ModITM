FROM ollama/ollama:latest

RUN apt update && apt-get install -y curl tcpdump iproute2

COPY startup.sh .

ENTRYPOINT ["./startup.sh"]