import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from django_socio_grpc.mixins import (
    CreateModelMixin,
    ListModelMixin,
    StreamModelMixin,
    get_default_grpc_messages,
    get_default_grpc_methods,
)


class UnitTestModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=100)
    # test

    class Meta:
        grpc_messages = {
            **get_default_grpc_messages("UnitTestModel"),
            **StreamModelMixin.get_default_message("UnitTestModel"),
        }

        grpc_methods = {
            **get_default_grpc_methods("UnitTestModel"),
            **StreamModelMixin.get_default_method("UnitTestModel"),
        }


class ForeignModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        ###################################
        # Simulate a retrieve by name     #
        # Simulate a read only model      #
        ###################################
        grpc_messages = {
            **CreateModelMixin.get_default_message("ForeignModel"),
            **ListModelMixin.get_default_message("ForeignModel", pagination=True),
            "ForeignModelRetrieveRequestCustom": ["name"],
        }
        grpc_methods = {
            **ListModelMixin.get_default_method("ForeignModel"),
            "Retrieve": {
                "request": {
                    "is_stream": False,
                    "message": "ForeignModelRetrieveRequestCustom",
                },
                "response": {
                    "is_stream": False,
                    "message": "ForeignModelRetrieveRequestCustom",
                },
            },
        }


class ManyManyModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)


class RelatedFieldModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foreign = models.ForeignKey(
        ForeignModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="related",
    )
    many_many = models.ManyToManyField(ManyManyModel, blank=True, related_name="relateds")

    class Meta:
        ###############################################################
        # Manually add many_many to serializer and a custom field     #
        ###############################################################
        grpc_messages = {
            **get_default_grpc_messages("RelatedFieldModel"),
            "RelatedFieldModelListResponse": [
                "uuid",
                "foreign",
                "many_many",
                "__custom__string__custom_field_name__",
                "__custom__repeated string__list_custom_field_name__",
            ],
        }

        grpc_methods = {
            **get_default_grpc_methods("RelatedFieldModel"),
            "List": {
                "request": {
                    "message": "RelatedFieldModelListRequest",
                },
                "response": {
                    "message": "RelatedFieldModelListResponse",
                },
            },
        }


class NotDisplayedModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        grpc_messages = {}
        grpc_methods = {}


class SpecialFieldsModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meta_datas = models.JSONField(
        default=dict,
        blank=True,
    )
    list_datas = ArrayField(
        models.IntegerField(),
        default=list,
        blank=True,
    )


class ImportStructEvenInArrayModel(models.Model):
    this_is_crazy = ArrayField(
        models.JSONField(
            default=dict,
            blank=True,
        ),
        default=list,
        blank=True,
    )

    class Meta:
        grpc_messages = {"ImportStructEvenInArrayModel": "__all__"}
        grpc_methods = {}
