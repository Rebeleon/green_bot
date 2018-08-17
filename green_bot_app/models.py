from django.db import models


class UserTelegramBot(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)
    buyer = models.BooleanField(default=False)
    order = models.IntegerField()
   # voted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
   # user_telegram_bot = models.ForeignKey(UserTelegramBot, on_delete=models.CASCADE)
   # choice = models.CharField(max_length=100)
    message_id = models.IntegerField(null=True)
    counter = models.IntegerField(default=0)
