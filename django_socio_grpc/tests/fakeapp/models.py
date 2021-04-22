import uuid

from django.db import models

from django_socio_grpc.mixins import (
    CreateModelMixin,
    ListModelMixin,
    get_default_grpc_messages,
    get_default_grpc_methods,
)


class UnitTestModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=100)
    # test


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
        ############################################
        # Manually add many_many to serializer     #
        ############################################
        grpc_messages = {
            **get_default_grpc_messages("RelatedFieldModel"),
            "RelatedFieldModelListResponse": ["uuid", "foreign", "many_many"],
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
