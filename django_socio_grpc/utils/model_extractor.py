from django.apps import apps
from django.contrib.contenttypes.models import ContentType


def get_app_list():
    """
    Get list of Django application as List
    """
    from django.apps import apps

    dict_app = {}

    for app in apps.get_app_configs():
        dict_app[app.name] = app.verbose_name

    return dict_app


def is_app_in_installed_app(app_name):
    """
    return true if an app is found in the installed app with the name passed as argument
    """
    return app_name in get_app_list()


def is_model_exist(model_name):
    return ContentType.objects.filter(model=model_name).exists()


def get_model(app_name, model_name):
    """
    Get Model from name
    """
    if app_name:
        return apps.get_model(app_label=app_name, model_name=model_name)
    else:
        #  ----------------------------------------------------------
        #  ---  search if this model exist on Django content type ---
        #  ----------------------------------------------------------
        current_model = ContentType.objects.filter(model=model_name).first()

        # -------------------------------
        # ---  This Model is valid    ---
        # -------------------------------
        if current_model:
            app_label = current_model.app_label
            current_model = apps.get_model(app_label=app_label, model_name=model_name)
            return current_model


def get_model_fields(model_object):
    """
    extract Column List from a Data Model
    """

    return model_object._meta.get_fields(
        include_parents=False
    )  # ---- get column list of the foreignkey Data Model ----
