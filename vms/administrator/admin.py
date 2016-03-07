from django.contrib import admin
from administrator.models import Administrator


class AdministratorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Administrator, AdministratorAdmin)