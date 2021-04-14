import grpc
import mock
import pytest
from django.test import TestCase, override_settings

from django_socio_grpc.exceptions import PermissionDenied
from django_socio_grpc.services import Service
from django_socio_grpc.settings import grpc_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeContext, FakeRpcError


class FakePermission:
    message = "fake message"
    code = "fake code"

    def has_permission(self, context, service):
        return True

    def has_object_permission(self, context, service, obj):
        return True


class DummyService(Service):
    pass


class TestPermissionUnitary(TestCase):
    @override_settings(
        GRPC_FRAMEWORK={
            "DEFAULT_PERMISSION_CLASSES": [
                "django_socio_grpc.tests.test_permissions.FakePermission",
            ],
        }
    )
    def test_settings(self):
        # test settings correctly passed to grpc_settings
        self.assertEqual(grpc_settings.DEFAULT_PERMISSION_CLASSES, [FakePermission])

    @mock.patch("django_socio_grpc.services.Service.get_permissions")
    def test_check_permissions_ok(self, mock_get_permissions):
        mock_get_permissions.return_value = [FakePermission()]
        #   Create a dummyservice for unitary tests
        dummy_service = DummyService()
        dummy_service.context = FakeContext()
        #   Call func
        with mock.patch(
            "django_socio_grpc.tests.test_permissions.FakePermission.has_permission"
        ) as mock_has_permissions:
            mock_has_permissions.return_value = True
            dummy_service.check_permissions()
            mock_has_permissions.assert_called_once_with(dummy_service.context, dummy_service)

    @mock.patch("django_socio_grpc.services.Service.get_permissions")
    def test_check_permissions_not_ok(self, mock_get_permissions):
        mock_get_permissions.return_value = [FakePermission()]
        mock_get_permissions.return_value = [FakePermission()]
        #   Create a dummyservice for unitary tests
        dummy_service = DummyService()
        dummy_service.context = FakeContext()
        #   Call func
        with mock.patch(
            "django_socio_grpc.tests.test_permissions.FakePermission.has_permission"
        ) as mock_has_permissions:
            mock_has_permissions.return_value = False
            with pytest.raises(PermissionDenied):
                dummy_service.check_permissions()
                mock_has_permissions.assert_called_once_with(
                    dummy_service.context, dummy_service
                )

    @mock.patch("django_socio_grpc.services.Service.get_permissions")
    def test_check_object_permissions_ok(self, mock_get_permissions):
        mock_get_permissions.return_value = [FakePermission()]
        #   Create a dummyservice for unitary tests
        dummy_service = DummyService()
        dummy_service.context = FakeContext()
        #   Call func
        with mock.patch(
            "django_socio_grpc.tests.test_permissions.FakePermission.has_object_permission"
        ) as mock_has_object_permissions:
            mock_has_object_permissions.return_value = True
            dummy_service.check_object_permissions("fake_obj")
            mock_has_object_permissions.assert_called_once_with(
                dummy_service.context, dummy_service, "fake_obj"
            )

    @mock.patch("django_socio_grpc.services.Service.get_permissions")
    def test_check_object_permissions_not_ok(self, mock_get_permissions):
        mock_get_permissions.return_value = [FakePermission()]
        #   Create a dummyservice for unitary tests
        dummy_service = DummyService()
        dummy_service.context = FakeContext()
        #   Call func
        with mock.patch(
            "django_socio_grpc.tests.test_permissions.FakePermission.has_object_permission"
        ) as mock_has_object_permissions:
            mock_has_object_permissions.return_value = False
            with pytest.raises(PermissionDenied):
                dummy_service.check_object_permissions("fake_obj")
                mock_has_object_permissions.assert_called_once_with(
                    dummy_service.context, dummy_service, "fake_obj"
                )

    def test_get_permissions(self):
        dummy_service = DummyService()
        dummy_service.permission_classes = [FakePermission]
        returned_perms = dummy_service.get_permissions()
        self.assertEqual(len(returned_perms), 1)
        self.assertIsInstance(returned_perms[0], FakePermission)

    @mock.patch("django_socio_grpc.services.Service.perform_authentication", mock.MagicMock())
    @mock.patch("django_socio_grpc.services.Service.check_permissions")
    def test_check_permissions_called_in_before_action(self, mock_check_permissions):
        dummy_service = DummyService()
        dummy_service.before_action()
        mock_check_permissions.assert_called_once_with()


class TestPermissionsIntegration(TestCase):
    def setUp(self):
        self.service = DummyService
        self.servicer = self.service.as_servicer()

        self.fake_context = FakeContext()

        def dummy_method(service, request, context):
            self.fake_context = context
            return "fake_result"

        self.dummy_method = dummy_method

    def test_permission_ok(self):
        self.service.permission_classes = [FakePermission]
        self.service.ListDummyMethod = self.dummy_method
        fake_result = self.servicer.ListDummyMethod(None, self.fake_context)
        self.assertEqual(fake_result, "fake_result")

    @mock.patch("django_socio_grpc.tests.test_permissions.FakePermission.has_permission")
    def test_permission_not_ok(self, mock_has_permissions):
        mock_has_permissions.return_value = False
        with self.assertRaises(FakeRpcError) as fake_rpc_error:
            self.service.permission_classes = [FakePermission]
            self.service.ListDummyMethod = self.dummy_method
            self.servicer.ListDummyMethod(None, self.fake_context)
        self.assertEqual(
            fake_rpc_error.exception._code, grpc.StatusCode.PERMISSION_DENIED.value
        )
        self.assertEqual(
            str(fake_rpc_error.exception._details),
            "{'message': ErrorDetail(string='fake message', code='permission_denied'), 'code': 'permission_denied'}",
        )

    def test_method_map_to_http_list(self):
        self.service.List = self.dummy_method
        self.servicer.List(None, self.fake_context)
        self.assertEqual(self.fake_context.method, "GET")

    def test_method_map_to_http_retrieve(self):
        self.service.Retrieve = self.dummy_method
        self.servicer.Retrieve(None, self.fake_context)
        self.assertEqual(self.fake_context.method, "GET")

    def test_method_map_to_http_create(self):
        self.service.Create = self.dummy_method
        self.servicer.Create(None, self.fake_context)
        self.assertEqual(self.fake_context.method, "POST")

    def test_method_map_to_http_update(self):
        self.service.Update = self.dummy_method
        self.servicer.Update(None, self.fake_context)
        self.assertEqual(self.fake_context.method, "PUT")

    def test_method_map_to_http_partial_update(self):
        self.service.PartialUpdate = self.dummy_method
        self.servicer.PartialUpdate(None, self.fake_context)
        self.assertEqual(self.fake_context.method, "PATCH")

    def test_method_map_to_http_destroy(self):
        self.service.Destroy = self.dummy_method
        self.servicer.Destroy(None, self.fake_context)
        self.assertEqual(self.fake_context.method, "DELETE")
