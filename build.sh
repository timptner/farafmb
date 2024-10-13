#!/usr/bin/env bash

log_step () {
    echo -e "\n>>>>> $1 <<<<<\n"
}

{
    log_step "pull debian image as base"
    container=$(buildah from debian)
    echo "new container: $container"

    log_step "install dependencies"
    buildah run $container -- apt-get update
    buildah run $container -- apt-get --yes install \
        python3 python3-dev python3-venv            \
        libpq-dev build-essential

    log_step "create application user"
    name=farafmb
    app_dir=/opt/$name
    buildah run $container -- useradd   \
        --shell /bin/bash               \
        --create-home                   \
        --home-dir $app_dir             \
        $name

    log_step "copy project files"
    buildah copy $container . $app_dir
    buildah run $container -- chown -R $name:$name $app_dir

    log_step "create service directories"
    public_dir=/srv/$name
    buildah run $container -- mkdir $public_dir
    buildah run $container -- chown -R $name:$name $public_dir
    buildah config --volume $public_dir $container

    log_step "set default user and working directory"
    buildah config              \
        --user $name            \
        --workingdir $app_dir   \
        $container

    log_step "install python packages"
    buildah run $container -- python3 -m venv .venv
    buildah run $container -- .venv/bin/pip install -r ./requirements.txt
    buildah run $container -- .venv/bin/pip install gunicorn

    log_step "collect static files"
    buildah config                              \
        --env STATIC_ROOT=$public_dir/static    \
        --env MEDIA_ROOT=$public_dir/media      \
        $container
    buildah run $container -- .venv/bin/python manage.py collectstatic --no-input

    log_step "configure server"
    port=8000
    run_cmd="$app_dir/.venv/bin/gunicorn --workers 2 --bind 0.0.0.0:$port farafmb.wsgi"
    buildah config                              \
        --cmd "$run_cmd"                        \
        --port $port                            \
        --env LOG_FILE=$app_dir/farafmb.log     \
        $container

    log_step "commit container as new image"
    image=$(buildah commit --rm $container "farafmb")

} >&2

echo $image
