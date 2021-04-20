# Fachschaftsrat Maschinenbau

[![Website status](https://img.shields.io/website?down_color=red&down_message=down&up_color=green&up_message=up&url=https%3A%2F%2Ffarafmb.de)](https://farafmb.de)
[![Mozilla Observatory](https://img.shields.io/mozilla-observatory/grade/farafmb.de?publish)](https://observatory.mozilla.org/analyze/farafmb.de)
[![Deployment status](https://img.shields.io/github/deployments/aiventimptner/farafmb/farafmb)](https://github.com/aiventimptner/farafmb/deployments/activity_log?environment=farafmb)
[![License](https://img.shields.io/github/license/aiventimptner/farafmb)](https://github.com/aiventimptner/farafmb/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/780487319936303114)](https://discord.gg/m9SutXWdnc)
[![Last commit](https://img.shields.io/github/last-commit/aiventimptner/farafmb/main)](https://github.com/aiventimptner/farafmb/commits/main)
![Code size](https://img.shields.io/github/languages/code-size/aiventimptner/farafmb)

This repository contains the source code for the homepage of [Fachschaftsrat Maschinenbau](https://farafmb.de) 
(FaRaFMB). FaRaFMB is the student representative for the faculty of mechanical engineering at the 
[Otto-von-Guericke-University Magdeburg](https://www.ovgu.de).

The website makes use of [Django](https://www.djangoproject.com/) and is styled with [Bulma](https://bulma.io/).

## Installation

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

Make sure to export all environment variables listed below before continuing with [#Run your server](#run-your-server).

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
