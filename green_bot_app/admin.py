from django.contrib import admin

from .models import Organisation, TelegramUser


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'buyer', 'phone_number')


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id_telegram', 'first_name', 'last_name', 'voted')


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
