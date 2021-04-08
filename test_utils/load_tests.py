import os
import sys

from test_utils.boot_django import boot_django  # noqa

APPS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.join(APPS_DIR, "django_socio_grpc")
sys.path.append(APPS_DIR)


# call the django setup routine
boot_django()

default_labels = [
    "django_socio_grpc/tests/",
]

ignore_labels = ["django_socio_grpc/tests/grpc_test_utils/"]


def get_suite(labels=default_labels, verbosity=3):
    from test_utils.test_runner import PytestTestRunner

    runner = PytestTestRunner(verbosity=verbosity)
    failures = runner.run_tests(labels, ignore_labels)
    if failures:
        sys.exit(failures)


def launch():
    labels = default_labels
    if len(sys.argv[1:]) > 0:
        labels = sys.argv[1:]
    get_suite(labels)


if __name__ == "__main__":
    launch()
