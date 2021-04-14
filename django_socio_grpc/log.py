"""
logging utils
"""
import logging
import logging.config

from django.core.management.color import color_style
from django.utils.module_loading import import_string

DEFAULT_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django_socio_grpc": {
            "()": "grpc_framework.utils.log.ServerFormatter",
            "format": "[{server_time}] {message} {resp_code} {resp_time}",
            "style": "{",
        }
    },
    "handlers": {
        "django_socio_grpc": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django_socio_grpc",
        },
    },
    "loggers": {
        "grpc": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django_socio_grpc": {
            "handlers": ["console", "django_socio_grpc"],
            "level": "INFO",
        },
    },
}


def configure_logging(logging_config, logging_settings):
    if logging_config:
        logging_config_func = import_string(logging_config)

        logging.config.dictConfig(DEFAULT_LOGGING)

        if logging_settings:
            logging_config_func(logging_settings)


class ServerFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.style = color_style()
        super().__init__(*args, **kwargs)

    def format(self, record):
        msg = record.msg
        code = getattr(record, "resp_code", None)
        if code:
            if code == "success":
                msg = self.style.HTTP_SUCCESS(msg)
            else:
                msg = self.style.HTTP_SERVER_ERROR(msg)

        if self.uses_server_time() and not hasattr(record, "server_time"):
            record.server_time = self.formatTime(record, self.datefmt)

        record.msg = msg
        return super().format(record)

    def uses_server_time(self):
        return self._fmt.find("{server_time}") >= 0
