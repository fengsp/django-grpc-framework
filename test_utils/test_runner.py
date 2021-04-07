import pytest


class PytestTestRunner:
    """Runs pytest to discover and run tests."""

    def __init__(self, verbosity=1, failfast=False, keepdb=False, show_local=False, **kwargs):
        self.verbosity = verbosity
        self.failfast = failfast
        self.keepdb = keepdb
        self.show_local = show_local

    def run_tests(self, test_labels, ignore_labels=[]):
        """Run pytest and return the exitcode.

        It translates some of Django's test command option to pytest's.
        """

        argv = []
        if self.verbosity == 0:
            argv.append("--quiet")
        if self.verbosity == 2:
            argv.append("--verbose")
        if self.verbosity == 3:
            argv.append("-vv")
        if self.failfast:
            argv.append("--exitfirst")
        if self.keepdb:
            argv.append("--reuse-db")
        if self.show_local:
            argv.append("-l")

        for ignore_label in ignore_labels:
            # argv.append(f"--ignore={ignore_label}")
            argv.append("--ignore")
            argv.append(ignore_label)

        argv.extend(test_labels)
        return pytest.main(argv)
