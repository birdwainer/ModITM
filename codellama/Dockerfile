FROM ollama/ollama:latest

RUN apt-get install -y curl

COPY startup.sh .

ENTRYPOINT ["./startup.sh"]