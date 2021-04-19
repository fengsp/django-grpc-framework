from django.db import models


class UnitTestModel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    text = models.CharField(max_length=100)
    # test
