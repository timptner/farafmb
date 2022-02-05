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

## Installation

Setup a local development environment with virtualenv. Activate it and install 
all package dependencies.

```bash
python3 -m venv ./env
source env/bin/activate
python -m pip install -r requirements.txt
```

Create a copy of `.env.example` and call it `.env`. Uncomment the second line 
which holds the value for `DJANGO_SETTINGS_MODULE`. Generate a new random 
secret key and fill out all empty values for the specified keys. You can use a 
django utility function to generate the secret key.

```python
#!/usr/bin/env python3
from django.core.management import utils
utils.get_random_secret_key()
```

To start your development server:

```bash
python manage.py runserver
```

When developing on the oauth provider (especially OIDC) you need to generate a 
new RSA key and use it as an environment variable.

```bash
# Generate new RSA key
openssl genrsa --out oidc.key 4096
# Set env var from file content
export OIDC_RSA_PRIVATE_KEY=$(cat oidc.key)
```

## License

[MIT](https://github.com/aiventimptner/farafmb.de/blob/main/LICENSE)
