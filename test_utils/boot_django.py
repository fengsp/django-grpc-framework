# File sets up the django environment, used by other scripts that need to
# execute in django land
import os
import sys

import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FAKE_APP_DIR = os.path.join(BASE_DIR, "django_socio_grpc", "tests")

sys.path.append(BASE_DIR)
sys.path.append(FAKE_APP_DIR)


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        GRPC_FRAMEWORK={
            "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination"
        },
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
            "django.contrib.contenttypes",
            "django_filters",
            "django_socio_grpc",
            "fakeapp",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
