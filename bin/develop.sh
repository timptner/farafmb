#!/usr/bin/env bash

podman run \
    --detach \
    --restart always \
    --publish 5432:5432 \
    --env 'POSTGRES_PASSWORD=secret' \
    --env 'POSTGRES_USER=farafmb' \
    --env 'POSTGRES_DB=farafmb' \
    --name farafmb \
    docker.io/library/postgres
