from django.db import models


class Snippet(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=20, null=True)
