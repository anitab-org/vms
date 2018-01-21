# Django
from administrator.models import Administrator

# local Django
from django.contrib import admin


class AdministratorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Administrator, AdministratorAdmin)
