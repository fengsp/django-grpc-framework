from unittest.mock import mock_open, patch

from django.core.management import call_command
from django.test import TestCase

expected_result = """syntax = "proto3";

package unittestmodel;

import "google/protobuf/empty.proto";

service UnitTestModelController {
    rpc List(UnitTestModelListRequest) returns (stream UnitTestModel) {}
    rpc Create(UnitTestModel) returns (UnitTestModel) {}
    rpc Retrieve(UnitTestModelRetrieveRequest) returns (UnitTestModel) {}
    rpc Update(UnitTestModel) returns (UnitTestModel) {}
    rpc Destroy(UnitTestModel) returns (google.protobuf.Empty) {}
}

message UnitTestModel {
    int32 id = 1;
    string title = 2;
    string text = 3;
}

message UnitTestModelListRequest {
}

message UnitTestModelRetrieveRequest {
    int32 id = 1;
}
"""


class TestProtoGeneration(TestCase):
    def test_mycommand(self):

        self.maxDiff = None

        args = []
        opts = {"model": "unittestmodel", "file": "proto/unittestmodel.proto"}
        with patch("builtins.open", mock_open()) as m:
            call_command("generateproto", *args, **opts)

        m.assert_called_once_with("proto/unittestmodel.proto", "w")
        handle = m()

        called_with_data = handle.write.call_args[0][0]
        self.assertEqual(called_with_data, expected_result)
