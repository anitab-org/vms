from django.contrib import admin
from shift.models import Shift
from shift.models import VolunteerShift


class ShiftAdmin(admin.ModelAdmin):
    pass
admin.site.register(Shift, ShiftAdmin)


class VolunteerShiftAdmin(admin.ModelAdmin):
    pass
admin.site.register(VolunteerShift, VolunteerShiftAdmin)
