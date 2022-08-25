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

## Installation 🛠️

### Development 🔧

Setup a local development environment with virtualenv. Activate it and install
all package dependencies.

```shell
python3 -m venv ./venv
source venv/bin/activate
python -m pip install -r requirements/development.txt
```

Create a copy of `.env.example` and call it `.env`. Generate a new random
secret key and fill out all empty values for the specified keys. You can use 
django's utility function to generate the secret key.

```shell
python manage.py shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"
```

To start your development server:

```shell
python manage.py runserver
```

When developing on the oauth provider (especially OIDC) you need to generate a
new RSA key and use it as an environment variable.

```shell
# Generate new RSA key
openssl genrsa --out oidc.key 4096
# Set env var from file content
export OIDC_RSA_PRIVATE_KEY=$(cat oidc.key)
```

At last, you should migrate the database and create a user.

```shell
python manage.py migrate
python manage.py createsuperuser
```

### Production 🌍

⚠️ **Follow all steps mentioned in
[Development](https://github.com/timptner/farafmb#Development)!** ⚠️️

Set `DJANGO_SETTINGS_MODULE` to `farafmb.settings.production` and change the
other variables as needed. Create a new RSA-Key and add it to your `.env`.

Configure [Gunicorn](https://docs.gunicorn.org/en/latest/deploy.html) as your
application server and [Nginx](https://nginx.org/en/docs/http/load_balancing.html)
as web server / proxy.

## Testing 🧪

Run tests with:

```shell
coverage run manage.py test
coverage html  # Update report
```

Afterwards open your browser and go to `file://<absolute_path_to_project_root>/htmlcov/index.html`

## Localization

At the moment only german localization is supported on this project. Actually german is used as the primary language and
english as the secondary but in the source code it is vice versa because of the intended implementation of Django.

To generate the files containing all string to localize run:

```shell
django-admin makemessages --locale "de" --ignore "venv/*"
```

And to compile the localized strings into binary data, which is used by gnugettext run:

```shell
django-admin compilemessages --locale "de" --ignore "venv/*"
```

## License 📚

[MIT](https://github.com/timptner/farafmb/blob/main/LICENSE)
