# Django
from django.contrib import admin

# local Django
from job.models import Job


class JobAdmin(admin.ModelAdmin):
    pass


admin.site.register(Job, JobAdmin)
