# Django
from django.contrib import admin

# local Django
from organization.models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organization, OrganizationAdmin)
