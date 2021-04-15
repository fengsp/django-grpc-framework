"""
Settings for gRPC framework are all namespaced in the GRPC_FRAMEWORK setting.
For example your project's `settings.py` file might look like this:

GRPC_FRAMEWORK = {
    'ROOT_HANDLERS_HOOK': 'path.to.my.custom_grpc_handlers',

    'SERVER_INTERCEPTORS': [Interceptor1(), Interceptor2()],

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    # default pagination class
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.Pagenumberpagination'

    'DEFAULT_AUTHENTICATION_CLASSES': ['path.to.AuthenticationClass'],

    'DEFAULT_PERMISSION_CLASSES': ['path.to.DefaultPermissionClass'],
}

This module provides the `grpc_setting` object, that is used to access
gRPC framework settings, checking for user settings first, then falling
back to the defaults.
"""
from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    #  Root grpc handlers hook configuration
    "ROOT_HANDLERS_HOOK": None,
    #  gRPC server configuration
    "SERVER_INTERCEPTORS": None,
    #  Default servicer authentication classes
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    # Default filter class
    "DEFAULT_FILTER_BACKENDS": [],
    # default pagination class
    "DEFAULT_PAGINATION_CLASS": None,
    #  Default permission classes
    "DEFAULT_PERMISSION_CLASSES": [],
    # gRPC running mode
    "GRPC_ASYNC": False,
    #  Default grpc channel port
    "GRPC_CHANNEL_PORT": 50051,
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = [
    "ROOT_HANDLERS_HOOK",
    "SERVER_INTERCEPTORS",
    "DEFAULT_AUTHENTICATION_CLASSES",
    "DEFAULT_PERMISSION_CLASSES",
]


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        # We need the ROOT_URLCONF so we do this lazily
        if setting_name == "ROOT_HANDLERS_HOOK":
            return import_from_string(
                "%s.grpc_handlers" % settings.ROOT_URLCONF,
                setting_name,
            )
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        raise ImportError(
            "Could not import '%s' for GRPC setting '%s'. %s: %s."
            % (val, setting_name, e.__class__.__name__, e)
        )


class GRPCSettings:
    """
    A settings object that allows gRPC Framework settings to be accessed as
    properties. For example:

        from django_socio_grpc.settings import grpc_settings
        print(grpc_settings.ROOT_HANDLERS_HOOK)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "GRPC_FRAMEWORK", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid gRPC setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


grpc_settings = GRPCSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_grpc_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "GRPC_FRAMEWORK" or setting == "ROOT_URLCONF":
        grpc_settings.reload()


setting_changed.connect(reload_grpc_settings)
