# Django
from django.contrib import admin

# local Django
from shift.models import Shift, VolunteerShift, EditRequest, Report


class ShiftAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shift, ShiftAdmin)


class VolunteerShiftAdmin(admin.ModelAdmin):
    pass


admin.site.register(VolunteerShift, VolunteerShiftAdmin)


class EditRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(EditRequest, EditRequestAdmin)


class ReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(Report, ReportAdmin)

