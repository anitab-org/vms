from django.contrib import admin
from volunteer.models import Volunteer


class VolunteerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Volunteer, VolunteerAdmin)
