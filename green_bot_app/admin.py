from django.contrib import admin, messages
from .models import Organisation, TelegramUser, DoorUsage


def change_buyer(modeladmin, request, queryset):
    if len(queryset) == 1:
        Organisation.objects.filter(buyer=True).update(buyer=False)
        queryset.update(buyer=True)
    else:
        messages.warning(request, "Отклонено. Выберите только одного")


change_buyer.short_description = 'Изменить покупателя'


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'buyer', 'phone_number', 'opened_door_time')
    actions = [change_buyer, ]


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id_telegram', 'first_name', 'last_name', 'voted', 'can_open_door')


class DoorUsageAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'request_door_time', 'opened_door')


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(DoorUsage, DoorUsageAdmin)
