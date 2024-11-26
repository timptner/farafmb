#!/usr/bin/env bash

podman pod create --name farafmb --publish 127.0.0.1:8000:8000

podman run --pod farafmb --detach --restart always  \
    --env 'POSTGRES_DB=farafmb'                     \
    --env 'POSTGRES_USER=farafmb'                   \
    --env 'POSTGRES_PASSWORD=secret'                \
    --volume 'farafmb-db:/var/lib/postgresql/data'  \
    docker.io/library/postgres:latest

container=$(                                            \
    podman run --pod farafmb --detach --restart always  \
    --env 'SECRET_KEY=secret'                           \
    --volume 'farafmb-static:/var/www/static'           \
    --volume 'farafmb-media:/var/www/media'             \
    --volume 'farafmb-logs:/var/log/farafmb'            \
    localhost/farafmb                                   \
)

podman exec $container .venv/bin/python3 manage.py migrate
podman exec $container \
    .venv/bin/python3 manage.py collectstatic --no-input --clear
