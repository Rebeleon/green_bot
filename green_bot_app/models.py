from django.db import models


class Name(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return self.phone_number


class CurrentBuyer(models.Model):
    buyer = models.CharField(max_length=200)

    def __str__(self):
        return self.buyer


class Order(models.Model):
    order = models.IntegerField()

    def __str__(self):
        return self.order
