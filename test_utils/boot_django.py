# File sets up the django environment, used by other scripts that need to
# execute in django land
import os
import sys

import django
from django.conf import settings

APPS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.join(APPS_DIR, "django_socio_grpc")

sys.path.append(APPS_DIR)


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.environ.get("DB_NAME"),
                "USER": os.environ.get("DB_USER"),
                "PASSWORD": os.environ.get("DB_PASSWORD"),
                "HOST": os.environ.get("DB_HOST"),
                "PORT": os.environ.get("DB_PORT", 5432),
            }
        },
        INSTALLED_APPS=(
            "rest_framework",
            # "django.contrib.contenttypes",
            "django_filters",
            "django_socio_grpc",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
