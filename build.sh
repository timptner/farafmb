#!/usr/bin/env bash

# create base image
container=$(buildah from debian)

# install dependencies
buildah run $container -- apt-get update
buildah run $container -- apt-get --yes install \
    python3 python3-dev python3-venv            \
    libpq-dev build-essential

# create app user
name=farafmb
app_dir=/opt/$name
buildah run $container -- useradd   \
    --shell /bin/bash               \
    --home-dir $app_dir $name
buildah config --user $name --workingdir $app_dir $container

# copy project
buildah copy --user $name $container . $app_dir

# install python depdencies
buildah run --user $name $container -- python3 -m venv .venv
buildah run --user $name $container -- .venv/bin/python3 -m \
    pip install -r ./requirements.txt
buildah run --user $name $container -- .venv/bin/python3 -m \
    pip install gunicorn

# create public dir
public_dir=/srv/$name
buildah run $container -- mkdir $public_dir
buildah run $container -- chown -R $name:$name $public_dir
buildah config --volume $public_dir $container

# collect static files
buildah config                              \
    --env STATIC_ROOT=$public_dir/static    \
    --env MEDIA_ROOT=$public_dir/media      \
    $container
buildah run --user $name $container -- .venv/bin/python3 manage.py collectstatic --no-input

# configure container
port=8000
run_cmd="$app_dir/.venv/bin/gunicorn --workers 2 --bind 0.0.0.0:$port farafmb.wsgi"
buildah config                              \
    --cmd $run_cmd                          \
    --port $port                            \
    --env LOG_FILE=$public_dir/server.log   \
    $container

# commit container as new image
buildah commit $container "farafmb"
