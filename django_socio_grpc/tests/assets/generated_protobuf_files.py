SIMPLE_MODEL_GENERATED = """syntax = "proto3";

package unittestmodel;

import "google/protobuf/empty.proto";

service UnitTestModelController {
    rpc List(UnitTestModelListRequest) returns (UnitTestModelListResponse) {}
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

message UnitTestModelListResponse {
    repeated UnitTestModel results = 1;
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
    rpc List(UnitTestModelListRequest) returns (UnitTestModelListResponse) {}
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

message UnitTestModelListResponse {
    repeated UnitTestModel results = 1;
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
    rpc List(UnitTestModelListRequest) returns (UnitTestModelListResponse) {}
    rpc Create(UnitTestModel) returns (UnitTestModel) {}
    rpc Retrieve(UnitTestModelRetrieveRequest) returns (UnitTestModel) {}
    rpc Update(UnitTestModel) returns (UnitTestModel) {}
    rpc Destroy(UnitTestModelDestroyRequest) returns (google.protobuf.Empty) {}
}

service ForeignModelController {
    rpc List(ForeignModelListRequest) returns (ForeignModelListResponse) {}
    rpc Retrieve(ForeignModelRetrieveRequestCustom) returns (ForeignModelRetrieveRequestCustom) {}
}

service ManyManyModelController {
    rpc List(ManyManyModelListRequest) returns (ManyManyModelListResponse) {}
    rpc Create(ManyManyModel) returns (ManyManyModel) {}
    rpc Retrieve(ManyManyModelRetrieveRequest) returns (ManyManyModel) {}
    rpc Update(ManyManyModel) returns (ManyManyModel) {}
    rpc Destroy(ManyManyModelDestroyRequest) returns (google.protobuf.Empty) {}
}

service RelatedFieldModelController {
    rpc List(RelatedFieldModelListRequest) returns (RelatedFieldModelListResponse) {}
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

message UnitTestModelListResponse {
    repeated UnitTestModel results = 1;
}

message UnitTestModelRetrieveRequest {
    int32 id = 1;
}

message UnitTestModelDestroyRequest {
    int32 id = 1;
}

message ForeignModel {
    string uuid = 1;
    string name = 2;
}

message ForeignModelListRequest {
}

message ForeignModelListResponse {
    repeated ForeignModel results = 1;
    int32 count = 2;
}

message ForeignModelRetrieveRequestCustom {
    string name = 1;
}

message ManyManyModel {
    string uuid = 1;
    string name = 2;
}

message ManyManyModelListRequest {
}

message ManyManyModelListResponse {
    repeated ManyManyModel results = 1;
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
}

message RelatedFieldModelListRequest {
}

message RelatedFieldModelListResponse {
    string uuid = 1;
    string foreign = 2;
    repeated string many_many = 3;
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
    rpc List(ForeignModelListRequest) returns (ForeignModelListResponse) {}
    rpc Retrieve(ForeignModelRetrieveRequestCustom) returns (ForeignModelRetrieveRequestCustom) {}
}

message ForeignModel {
    string uuid = 1;
    string name = 2;
}

message ForeignModelListRequest {
}

message ForeignModelListResponse {
    repeated ForeignModel results = 1;
    int32 count = 2;
}

message ForeignModelRetrieveRequestCustom {
    string name = 1;
}

"""

MODEL_WITH_M2M_GENERATED = """syntax = "proto3";

package fakeapp;

import "google/protobuf/empty.proto";

service RelatedFieldModelController {
    rpc List(RelatedFieldModelListRequest) returns (RelatedFieldModelListResponse) {}
    rpc Create(RelatedFieldModel) returns (RelatedFieldModel) {}
    rpc Retrieve(RelatedFieldModelRetrieveRequest) returns (RelatedFieldModel) {}
    rpc Update(RelatedFieldModel) returns (RelatedFieldModel) {}
    rpc Destroy(RelatedFieldModelDestroyRequest) returns (google.protobuf.Empty) {}
}

message RelatedFieldModel {
    string uuid = 1;
    string foreign = 2;
}

message RelatedFieldModelListRequest {
}

message RelatedFieldModelListResponse {
    string uuid = 1;
    string foreign = 2;
    repeated string many_many = 3;
}

message RelatedFieldModelRetrieveRequest {
    string uuid = 1;
}

message RelatedFieldModelDestroyRequest {
    string uuid = 1;
}

"""
