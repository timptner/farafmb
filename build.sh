#!/usr/bin/env bash

# create base image
container=$(buildah from debian)

# install dependencies
buildah run "$container" -- apt-get update
buildah run "$container" -- apt-get -y install python3 python3-dev python3-venv libpq-dev build-essential

# create app directory
buildah copy "$container" . /opt/farafmb
buildah config --workingdir /opt/farafmb "$container"

# install python depdencies
buildah run "$container" -- python3 -m venv .venv
buildah run "$container" -- .venv/bin/python3 -m pip install -r ./requirements.txt
buildah run "$container" -- .venv/bin/python3 -m pip install gunicorn

# add run command and expose ports
buildah config --cmd "/opt/farafmb/.venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8000 farafmb.wsgi" "$container"
buildah config --port 8000 "$container"

# commit container as new image
buildah commit "$container" "timptner/farafmb"
