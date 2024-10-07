# Fachschaftsrat Maschinenbau

[![Build](https://github.com/timptner/farafmb/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/timptner/farafmb/actions/workflows/build.yaml)
[![Size](https://img.shields.io/github/repo-size/timptner/farafmb)](https://github.com/timptner/farafmb)
[![License](https://img.shields.io/github/license/timptner/farafmb)](https://github.com/timptner/farafmb/blob/main/LICENSE)

This repository contains the source code for the homepage of
[Fachschaftsrat Maschinenbau](https://farafmb.de) (FaRaFMB). FaRaFMB is the
student representative for the faculty of mechanical engineering at the
[Otto von Guericke University Magdeburg](https://www.ovgu.de).

The website is build with [Django](https://www.djangoproject.com/) and uses
[Bulma](https://bulma.io/) for styling.

## Develop

Setup a local environment with virtualenv. Activate it and install all
dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install coverage
```

Create a new config file for env vars. Update values as required. Generate a
new secret key and place it in your config.

```bash
cp .env.example .env
python3 -c "from django.core.management import utils; print(utils.get_random_secret_key())"
```

Migrate the database, create an admin account and finally start your
development server.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Do not forget to write A LOT of tests. Always increase test coverage.

```bash
coverage run manage.py test
coverage report --skip-covered
```

## Build

Images are build using
[buildah](https://github.com/containers/buildah/blob/main/install.md). The
build skript needs to be run as root.

```bash
sudo -s
./build.sh
```

Afterwards you can run your image with podman (still as root). Provide env vars
with `--env "KEY=VALUE"` or `--env-file /path/to/.env`.

```bash
podman run --rm --detach --publish 127.0.0.1:8000:8000 --name farafmb localhost/timptner/farafmb
```

## Deploy

// TODO

- Use [nginx](https://nginx.org/en/docs/http/load_balancing.html) as proxy
- Use _postgres_ as database
- Share volumes for persistent storage and serve static files via _nginx_
- Add https with _certbot_
- Add backups with _borg_ (include pg_dump and volumes)
- Add logs and setup logrotation

## Localization

At the moment only german localization is supported on this project. Actually german is used as the primary language and
english as the secondary but in the source code it is vice versa because of the intended implementation of Django.

To generate the files containing all string to localize run:

```bash
django-admin makemessages --locale "de" --ignore "venv/*"
```

And to compile the localized strings into binary data, which is used by gnugettext run:

```bash
django-admin compilemessages --locale "de" --ignore "venv/*"
```

## License

[MIT](https://github.com/timptner/farafmb/blob/main/LICENSE)
