#!/usr/bin/env bash

# pull base image
container=$(buildah from debian)

# install dependencies
buildah run $container -- apt-get update
buildah run $container -- apt-get --yes install \
    python3 python3-dev python3-venv            \
    libpq-dev build-essential

# create application user
name=farafmb
app_dir=/opt/$name
buildah run $container -- useradd   \
    --shell /bin/bash               \
    --create-home                   \
    --home-dir $app_dir             \
    $name

# copy project files
buildah copy $container . $app_dir
buildah run $container -- chown -R $name:$name $app_dir

# create service directories
public_dir=/srv/$name
buildah run $container -- mkdir $public_dir
buildah run $container -- chown -R $name:$name $public_dir
buildah config --volume $public_dir $container

# set default user and working directory
buildah config              \
    --user $name            \
    --workingdir $app_dir   \
    $container

# install python packages
buildah run $container -- python3 -m venv .venv
buildah run $container -- .venv/bin/pip install -r ./requirements.txt
buildah run $container -- .venv/bin/pip install gunicorn

# collect static files
buildah config                              \
    --env STATIC_ROOT=$public_dir/static    \
    --env MEDIA_ROOT=$public_dir/media      \
    --env LOG_FILE=$public_dir/farafmb.log  \
    $container
buildah run $container -- .venv/bin/python manage.py collectstatic --no-input

# configure server
port=8000
run_cmd="$app_dir/.venv/bin/gunicorn --workers 2 --bind 0.0.0.0:$port farafmb.wsgi"
buildah config                              \
    --cmd "$run_cmd"                        \
    --port $port                            \
    $container

# publish image
image=$(buildah commit --rm $container "farafmb")
buildah login --username $GITHUB_USER --password $GITHUB_TOKEN ghcr.io
buildah push $image ghcr.io/$REPO_OWNER/farafmb:$VERSION_TAG
