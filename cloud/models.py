from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    title = models.CharField(max_length=25)
    file = models.FileField()

    def __str__(self):
        return self.title


class Item(models.Model):
    name = models.CharField(max_length=25)
    datetime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    files = models.ManyToManyField(File)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
