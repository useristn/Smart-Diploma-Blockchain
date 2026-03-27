from django.contrib import admin

from reports.models import ReportExport


@admin.register(ReportExport)
class ReportExportAdmin(admin.ModelAdmin):
    list_display = ("report_type", "requested_by", "created_at")

# Register your models here.
