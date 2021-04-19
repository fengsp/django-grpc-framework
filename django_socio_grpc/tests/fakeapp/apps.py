from django.apps import AppConfig


class FakeappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fakeapp"
