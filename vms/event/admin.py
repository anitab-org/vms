# Django
from django.contrib import admin

# local Django
from event.models import Event


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)
