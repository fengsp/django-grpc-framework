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
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            "rest_framework",
            # "django.contrib.contenttypes",
            "django_socio_grpc",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()
