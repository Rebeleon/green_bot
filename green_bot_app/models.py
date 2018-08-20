from django.db import models


class UserTelegramBot(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    buyer = models.BooleanField(default=False)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Vote(models.Model):
    message_id = models.IntegerField(null=True)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return str(self.message_id)


class TelegramUser(models.Model):
    id_telegram = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id_telegram)
