from django.contrib import admin

from .models import Name


class NameAdmin(admin.ModelAdmin):
    list_display = ('name','buyer','phone_number')


admin.site.register(Name, NameAdmin)
