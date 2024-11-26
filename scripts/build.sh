#!/usr/bin/env bash

# pull base image
container=$(buildah from alpine)

# install dependencies
buildah run $container -- apk update
buildah run $container -- apk add python3 python3-dev py3-pip libpq nodejs npm
buildah run $container -- npm install -g sass

# create application user
buildah run $container -- adduser -D farafmb

# copy project files into application directory
app_dir=/srv/farafmb
buildah copy $container . $app_dir
buildah run $container -- chown -R farafmb:farafmb $app_dir

# create volumes
static_dir=/var/www/static
buildah run $container -- mkdir --parents $static_dir
buildah run $container -- chown farafmb:farafmb $static_dir
buildah config --volume $static_dir $container

media_dir=/var/www/media
buildah run $container -- mkdir --parents $media_dir
buildah run $container -- chown farafmb:farafmb $media_dir
buildah config --volume $media_dir $container

log_dir=/var/log/farafmb
buildah run $container -- mkdir --parents $log_dir
buildah run $container -- chown farafmb:farafmb $log_dir
buildah config --volume $log_dir $container

# set default user and working directory
buildah config --user farafmb --workingdir $app_dir $container

# install python packages
buildah run $container -- python3 -m venv .venv
buildah run $container -- .venv/bin/python3 -m pip install -U pip
buildah run $container -- .venv/bin/python3 -m pip install -r requirements.txt
buildah run $container -- .venv/bin/python3 -m pip install gunicorn

# install node modules
buildah run $container -- npm install
buildah run $container -- npm run build

# configure container
cmd="$app_dir/.venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8000 farafmb.wsgi"
buildah config --port 8000 --cmd "$cmd"     \
    --env "STATIC_ROOT=$static_dir"         \
    --env "MEDIA_ROOT=$media_dir"           \
    --env "LOG_FILE=$log_dir/django.log"    \
    $container

# publish image
image=$(buildah commit $container "farafmb")
buildah login --username $GITHUB_USER --password $GITHUB_TOKEN ghcr.io
buildah tag $image $VERSION_TAG
buildah push $image ghcr.io/$REPO_OWNER/farafmb:latest
