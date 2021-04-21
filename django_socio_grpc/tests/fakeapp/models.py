import uuid

from django.db import models


class UnitTestModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=100)
    # test


class ForeignModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        grpc_messages = []
        grpc_methods = []


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
