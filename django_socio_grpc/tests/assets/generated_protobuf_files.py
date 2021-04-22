SIMPLE_MODEL_GENERATED = """syntax = "proto3";

package unittestmodel;

import "google/protobuf/empty.proto";

service UnitTestModelController {
    rpc List(UnitTestModelListRequest) returns (stream UnitTestModel) {}
    rpc Create(UnitTestModel) returns (UnitTestModel) {}
    rpc Retrieve(UnitTestModelRetrieveRequest) returns (UnitTestModel) {}
    rpc Update(UnitTestModel) returns (UnitTestModel) {}
    rpc Destroy(UnitTestModelDestroyRequest) returns (google.protobuf.Empty) {}
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

message UnitTestModelDestroyRequest {
    int32 id = 1;
}

"""

SIMPLE_APP_MODEL_NO_GENERATION = """syntax = "proto3";

package fakeapp;

import "google/protobuf/empty.proto";

"""

SIMPLE_APP_MODEL_GENERATED = """syntax = "proto3";

package fakeapp;

import "google/protobuf/empty.proto";

service UnitTestModelController {
    rpc List(UnitTestModelListRequest) returns (stream UnitTestModel) {}
    rpc Create(UnitTestModel) returns (UnitTestModel) {}
    rpc Retrieve(UnitTestModelRetrieveRequest) returns (UnitTestModel) {}
    rpc Update(UnitTestModel) returns (UnitTestModel) {}
    rpc Destroy(UnitTestModelDestroyRequest) returns (google.protobuf.Empty) {}
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

message UnitTestModelDestroyRequest {
    int32 id = 1;
}

"""

ALL_APP_GENERATED = """syntax = "proto3";

package fakeapp;

import "google/protobuf/empty.proto";

service UnitTestModelController {
    rpc List(UnitTestModelListRequest) returns (stream UnitTestModel) {}
    rpc Create(UnitTestModel) returns (UnitTestModel) {}
    rpc Retrieve(UnitTestModelRetrieveRequest) returns (UnitTestModel) {}
    rpc Update(UnitTestModel) returns (UnitTestModel) {}
    rpc Destroy(UnitTestModelDestroyRequest) returns (google.protobuf.Empty) {}
}

service ForeignModelController {
    rpc List(ForeignModelListRequest) returns (stream ForeignModel) {}
    rpc Retrieve(ForeignModelRetrieveRequestCustom) returns (ForeignModelRetrieveRequestCustom) {}
}

service ManyManyModelController {
    rpc List(ManyManyModelListRequest) returns (stream ManyManyModel) {}
    rpc Create(ManyManyModel) returns (ManyManyModel) {}
    rpc Retrieve(ManyManyModelRetrieveRequest) returns (ManyManyModel) {}
    rpc Update(ManyManyModel) returns (ManyManyModel) {}
    rpc Destroy(ManyManyModelDestroyRequest) returns (google.protobuf.Empty) {}
}

service RelatedFieldModelController {
    rpc List(RelatedFieldModelListRequest) returns (stream RelatedFieldModel) {}
    rpc Create(RelatedFieldModel) returns (RelatedFieldModel) {}
    rpc Retrieve(RelatedFieldModelRetrieveRequest) returns (RelatedFieldModel) {}
    rpc Update(RelatedFieldModel) returns (RelatedFieldModel) {}
    rpc Destroy(RelatedFieldModelDestroyRequest) returns (google.protobuf.Empty) {}
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

message UnitTestModelDestroyRequest {
    int32 id = 1;
}

message ForeignModelListRequest {
    string related = 1;
    string uuid = 2;
    string name = 3;
}

message ForeignModelRetrieveRequestCustom {
    string name = 1;
}

message ManyManyModel {
    string relateds = 1;
    string uuid = 2;
    string name = 3;
}

message ManyManyModelListRequest {
}

message ManyManyModelRetrieveRequest {
    string uuid = 1;
}

message ManyManyModelDestroyRequest {
    string uuid = 1;
}

message RelatedFieldModel {
    string uuid = 1;
    string foreign = 2;
    string many_many = 3;
}

message RelatedFieldModelListRequest {
}

message RelatedFieldModelRetrieveRequest {
    string uuid = 1;
}

message RelatedFieldModelDestroyRequest {
    string uuid = 1;
}

"""

CUSTOM_APP_MODEL_GENERATED = """syntax = "proto3";

package fakeapp;

import "google/protobuf/empty.proto";

service ForeignModelController {
    rpc List(ForeignModelListRequest) returns (stream ForeignModel) {}
    rpc Retrieve(ForeignModelRetrieveRequestCustom) returns (ForeignModelRetrieveRequestCustom) {}
}

message ForeignModelListRequest {
    string related = 1;
    string uuid = 2;
    string name = 3;
}

message ForeignModelRetrieveRequestCustom {
    string name = 1;
}

"""
