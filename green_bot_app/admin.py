from django.contrib import admin

from .models import UserTelegramBot, Vote, TelegramUser


class UserTelegramAdmin(admin.ModelAdmin):
    list_display = ('name', 'buyer', 'phone_number')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('counter', 'id', 'message_id')


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id_telegram', 'first_name', 'last_name', 'voted')


admin.site.register(UserTelegramBot, UserTelegramAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
