import sys

from boot_django import boot_django

# call the django setup routine
boot_django()

default_labels = [
    "django_socio_grpc/tests/",
]


def get_suite(labels=default_labels, verbosity=3):
    from test_runner import PytestTestRunner

    runner = PytestTestRunner(verbosity=verbosity)
    failures = runner.run_tests(labels)
    if failures:
        sys.exit(failures)


if __name__ == "__main__":
    labels = default_labels
    if len(sys.argv[1:]) > 0:
        labels = sys.argv[1:]
    get_suite(labels)
