# File sets up the django environment, used by other scripts that need to
# execute in django land
import os

import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "socotecio_sso"))


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
                "PORT": os.environ.get("DB_PORT"),
            }
        },
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "socotecio_sso",
        ),
        SOCOTECIO_SSO_RESOLVE_USER_SPECIFIC="socotecio_sso.tests.utils.mock_resolve_user_specific",
        OIDC_AUTH={"OIDC_RESOLVE_USER_FUNCTION": "socotecio_sso.auth.get_user_by_id"},
        TIME_ZONE="UTC",
        USE_TZ=True,
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.db.DatabaseCache",
                "LOCATION": "test_cache_table",
            }
        },
    )
    django.setup()
