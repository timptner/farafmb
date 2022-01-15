# Fachschaftsrat Maschinenbau

![Travis CI](https://img.shields.io/travis/com/aiventimptner/farafmb.de/main)
[![License](https://img.shields.io/github/license/aiventimptner/farafmb)](https://github.com/aiventimptner/farafmb/blob/main/LICENSE)
![Code size](https://img.shields.io/github/languages/code-size/aiventimptner/farafmb)

This repository contains the source code for the homepage of [Fachschaftsrat Maschinenbau](https://farafmb.de) 
(FaRaFMB). FaRaFMB is the student representative for the faculty of mechanical engineering at the 
[Otto von Guericke University Magdeburg](https://www.ovgu.de).

The website is build with [Django](https://www.djangoproject.com/) and uses [Bulma](https://bulma.io/) for styling.

## Installation

### Development

To develop in a local environment it is best to use [Docker](https://www.docker.com/) since we use a containerized 
setup in production. Follow the steps below to set up your dev environment.

1. Create a copy of `.env.example` and name it `.env`. Fill out all empty values and uncomment the last line.
2. Create a copy of `docker-compose.override.yaml.example` and name it `docker-compose.override.yaml`.

Start your local set up via `docker compose up`. If you run the startup command for the first time on a new machine you 
will need to migrate the database. Therefor you can execute typical django commands (like `python manage.py migrate`) 
with `docker compose exec farafmb <command>`. If you need an interactive shell from inside the container you can run 
`docker compose exec farafmb bash`.

### Production

It's strongly recommended to read the [documentation](https://docs.djangoproject.com/en/dev/) for Django! The following 
instructions are focused on a local installation to set up a development environment. Installation in a production 
environment should be handled by an advanced or professional sys-admin.

[Heroku](https://www.heroku.com/) can be used to allow easy deployment. Since the homepage is currently running on 
Heroku all needed adjustments for a deployment to heroku are already made.

### Requirements

- OpenSSL
- PostgreSQL

To build `psycopg2` one needs to have a local installation of postgresql. As an alternative one can install 
`psycopg2-binary` which can be used without building from source. Also, an updated version of OpenSSL is required.

If you're on a mac it's recommended to use [homebrew](https://brew.sh).

```shell
brew install openssl
brew install postgresql
```

### Dependencies

With all requirements available one can create a virtual environment and install all required dependencies.

```shell
python3 -m venv ./venv
source activate venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Make sure to export all environment variables listed below before continuing with 
[Run your local server](#run-your-local-server).

- DJANGO_SETTINGS_MODULE
  - Use `farafmb.settings_dev`  when in development environment
  - Defaults to `farafmb.settings` if not set
- SECRET_KEY
  - Django provides a helper function to generate a new secret key
    ```python
    from django.core.management import utils
    utils.get_random_secret_key()
    ```

When `DJANGO_SETTINGS_MODULE=farafmb.settings_dev` one can skip all `DB_*` variables because SQLite3 is used as 
database.

- DB_HOST
- DB_PORT
- DB_NAME
- DB_HOST_USER
- DB_HOST_PASSWORD

In local development one shouldn't send real emails. Therefore, use a service like [Mailtrap](https://mailtrap.io) or 
checkout the corresponding chapter in the 
[django documentation](https://docs.djangoproject.com/en/3.2/topics/email/#configuring-email-for-development).

- EMAIL_HOST
- EMAIL_PORT
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

### Run your local server

```shell
python manage.py migrate
python manage.py runserver
```

## License

[MIT](https://github.com/aiventimptner/farafmb/blob/main/LICENSE)
