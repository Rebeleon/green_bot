from django.db import models
from django.utils import timezone


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
    can_open_door = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id_telegram)


class DoorUsage(models.Model):
    id_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    request_door_time = models.DateTimeField('request_for_door')
    opened_door_time = models.DateTimeField('success_request', blank=True, default=None)

    def __str__(self):
        return str(self.request_door_time)
