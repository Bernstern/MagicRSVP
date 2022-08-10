#!/bin/bash

if [ $# -eq 0 ]
  then 
    echo "You need to pass the url of an elastic container registry to this script."
    exit
fi

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $1
DOCKER_BUILDKIT=1 docker build -t magic_rsvp .
docker tag covid_research:latest $1/magic_rsvp:latest
docker push $1/magic_rsvp:latest