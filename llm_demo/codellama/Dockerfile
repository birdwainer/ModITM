FROM ollama/ollama:0.1.27

RUN apt update && apt-get install -y curl tcpdump iproute2

COPY startup.sh .

ENTRYPOINT ["./startup.sh"]