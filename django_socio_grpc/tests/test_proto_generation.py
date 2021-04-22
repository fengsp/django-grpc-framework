from unittest.mock import mock_open, patch

from django.core.management import call_command
from django.test import TestCase

from django_socio_grpc.exceptions import ProtobufGenerationException

from .assets.generated_protobuf_files import (
    ALL_APP_GENERATED,
    CUSTOM_APP_MODEL_GENERATED,
    MODEL_WITH_M2M_GENERATED,
    SIMPLE_APP_MODEL_GENERATED,
    SIMPLE_APP_MODEL_NO_GENERATION,
    SIMPLE_MODEL_GENERATED,
)


class TestProtoGeneration(TestCase):
    def test_generate_one_model(self):
        self.maxDiff = None
        args = []
        opts = {"model": "unittestmodel", "file": "proto/unittestmodel.proto"}
        with patch("builtins.open", mock_open()) as m:
            call_command("generateproto", *args, **opts)

        m.assert_called_once_with("proto/unittestmodel.proto", "w")
        handle = m()

        called_with_data = handle.write.call_args[0][0]
        self.assertEqual(called_with_data, SIMPLE_MODEL_GENERATED)

    def test_raise_when_no_app_and_no_model_options(self):
        args = []
        opts = {}
        with self.assertRaises(ProtobufGenerationException) as fake_generation_error:
            call_command("generateproto", *args, **opts)

        self.assertEqual(
            str(fake_generation_error.exception),
            "Error on protobuf generation on model None on app None: You need to specify at least one app or one model",
        )

    def test_raise_when_app_not_found(self):
        args = []
        opts = {"app": "app_not_existing"}
        with self.assertRaises(ProtobufGenerationException) as fake_generation_error:
            call_command("generateproto", *args, **opts)

        self.assertEqual(
            str(fake_generation_error.exception),
            "Error on protobuf generation on model None on app app_not_existing: Invalid Django app",
        )

    def test_raise_when_model_not_found(self):
        args = []
        opts = {"model": "model_not_existing"}
        with self.assertRaises(ProtobufGenerationException) as fake_generation_error:
            call_command("generateproto", *args, **opts)

        self.assertEqual(
            str(fake_generation_error.exception),
            "Error on protobuf generation on model model_not_existing on app None: Invalid Django model",
        )

    def test_raise_when_file_exist_no_update(self):
        args = []
        opts = {"app": "fakeapp", "file": "proto/fakeapp.proto", "update": False}
        with self.assertRaises(ProtobufGenerationException) as fake_generation_error:
            call_command("generateproto", *args, **opts)

        self.assertEqual(
            str(fake_generation_error.exception),
            "Error on protobuf generation on model None on app fakeapp: File proto/fakeapp.proto already exist",
        )

    def test_generate_message_with_repeated_for_m2m(self):
        self.maxDiff = None

        args = []
        opts = {"app": "fakeapp", "model": "RelatedFieldModel"}
        with patch("builtins.open", mock_open()) as m:
            call_command("generateproto", *args, **opts)

        # this is done to avoid error on different absolute path
        assert m.mock_calls[0].args[0].endswith("fakeapp/grpc/fakeapp.proto")
        assert m.mock_calls[0].args[1] == "w"

        handle = m()

        called_with_data = handle.write.call_args[0][0]
        self.assertEqual(called_with_data, MODEL_WITH_M2M_GENERATED)

    def test_generate_one_app_one_model_no_message_no_methods(self):
        self.maxDiff = None

        args = []
        opts = {"app": "fakeapp", "model": "NotDisplayedModel"}
        with patch("builtins.open", mock_open()) as m:
            call_command("generateproto", *args, **opts)

        # this is done to avoid error on different absolute path
        assert m.mock_calls[0].args[0].endswith("fakeapp/grpc/fakeapp.proto")
        assert m.mock_calls[0].args[1] == "w"
        handle = m()

        called_with_data = handle.write.call_args[0][0]
        self.assertEqual(called_with_data, SIMPLE_APP_MODEL_NO_GENERATION)

    def test_generate_one_app_one_model(self):
        self.maxDiff = None
        args = []
        opts = {"app": "fakeapp", "model": "unittestmodel"}
        with patch("builtins.open", mock_open()) as m:
            call_command("generateproto", *args, **opts)

        # this is done to avoid error on different absolute path
        assert m.mock_calls[0].args[0].endswith("fakeapp/grpc/fakeapp.proto")
        assert m.mock_calls[0].args[1] == "w"

        handle = m()

        called_with_data = handle.write.call_args[0][0]
        self.assertEqual(called_with_data, SIMPLE_APP_MODEL_GENERATED)

    def test_generate_one_app_all_models(self):
        self.maxDiff = None

        args = []
        opts = {"app": "fakeapp"}
        with patch("builtins.open", mock_open()) as m:
            call_command("generateproto", *args, **opts)

        # this is done to avoid error on different absolute path
        assert m.mock_calls[0].args[0].endswith("fakeapp/grpc/fakeapp.proto")
        assert m.mock_calls[0].args[1] == "w"

        handle = m()

        called_with_data = handle.write.call_args[0][0]
        self.assertEqual(called_with_data, ALL_APP_GENERATED)

    def test_generate_one_app_one_model_customized(self):
        self.maxDiff = None
        args = []
        opts = {"app": "fakeapp", "model": "ForeignModel"}
        with patch("builtins.open", mock_open()) as m:
            call_command("generateproto", *args, **opts)

        # this is done to avoid error on different absolute path
        assert m.mock_calls[0].args[0].endswith("fakeapp/grpc/fakeapp.proto")
        assert m.mock_calls[0].args[1] == "w"

        handle = m()

        called_with_data = handle.write.call_args[0][0]
        self.assertEqual(called_with_data, CUSTOM_APP_MODEL_GENERATED)
