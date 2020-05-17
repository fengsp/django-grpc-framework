from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
