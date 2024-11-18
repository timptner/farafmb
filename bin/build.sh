#!/usr/bin/env bash

# pull base image
container=$(buildah from debian)

# install dependencies
buildah run $container -- apt-get update
buildah run $container -- apt-get --yes install \
    python3 python3-dev python3-venv            \
    libpq-dev build-essential

# create application user
buildah run $container -- useradd   \
    --shell /bin/bash               \
    --create-home                   \
    farafmb

# copy project files
buildah copy $container . /opt/farafmb
buildah run $container -- chown -R farafmb:farafmb /opt/farafmb

# create volume
buildah run $container -- mkdir /srv/farafmb
buildah run $container -- chown -R farafmb:farafmb /srv/farafmb
buildah config --volume /srv/farafmb $container

# set default user and working directory
buildah config                  \
    --user farafmb              \
    --workingdir /opt/farafmb   \
    $container

# install python packages
buildah run $container -- python3 -m venv .venv
buildah run $container -- .venv/bin/pip install -r requirements.txt
buildah run $container -- .venv/bin/pip install gunicorn

# configure container
run_cmd="/opt/farafmb/.venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8000 farafmb.wsgi"
buildah config                              \
    --env STATIC_ROOT=/srv/farafmb/static   \
    --env MEDIA_ROOT=/srv/farafmb/media     \
    --env LOG_FILE=/srv/farafmb/farafmb.log \
    --port 8000                             \
    --cmd "$run_cmd"                        \
    $container

# publish image
image=$(buildah commit $container "farafmb")
buildah login --username $GITHUB_USER --password $GITHUB_TOKEN ghcr.io
buildah tag $image $VERSION_TAG
buildah push $image ghcr.io/$REPO_OWNER/farafmb:latest
