from django.db import models


class Name(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    buyer = models.CharField(max_length=200)
    order = models.IntegerField()
    def __str__(self):
        return self.name
