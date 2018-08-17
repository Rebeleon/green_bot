from django.contrib import admin

from .models import UserTelegramBot, Vote


class UserTelegramAdmin(admin.ModelAdmin):
    list_display = ('name','buyer','phone_number')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('counter','id', 'message_id')


admin.site.register(UserTelegramBot, UserTelegramAdmin)
admin.site.register(Vote, VoteAdmin)