#! /bin/sh

for model in $(cat /model_puller/modelnames.txt)
do
    curl -X POST \
    -H "Content-Type: application/json" \
    -d "{ \"name\": \"$model\" }" \
    http://$OLLAMA_HOST:$OLLAMA_PORT/api/pull
done