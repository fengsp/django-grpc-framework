from django.test import TestCase, override_settings
from django.core.management import call_command
from .fakeapp.models import UnitTestModel
from .fakeapp.serializers import UnitTestSerializer

class TestProtoGeneration(TestCase):

    def test_mycommand(self):
        "Test my custom command."

        args = []
        opts = {
            "model": "UnitTestModel"
        }
        call_command('generateproto', *args, **opts)

        assert False