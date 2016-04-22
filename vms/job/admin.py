from django.contrib import admin
from job.models import Job


class JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Job, JobAdmin)
