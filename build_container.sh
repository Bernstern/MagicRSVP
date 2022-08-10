#!/bin/bash

DOCKER_BUILDKIT=1 docker build --pull --rm -f "dockerfile" -t magic_rsvp:latest "." 

printf "\nRun:\n\ncurl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'\n\nto kick the function.\n\n"

docker run -p 9000:8080 --env-file .env magic_rsvp:latest 