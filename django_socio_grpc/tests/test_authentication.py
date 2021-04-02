from django.test import TestCase


class FakeAuthentication:
    def authenticate(self, context):
        return ({"email": "john.doe@johndoe.com"}, {})


class TestAuthentication(TestCase):
    def test_sample(self):
        assert True
