from django.db import models


class Organisation(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    buyer = models.BooleanField(default=False)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class TelegramUser(models.Model):
    id_telegram = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id_telegram)
