from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class ReportExport(UUIDPrimaryKeyModel, TimeStampedModel):
    report_type = models.CharField(max_length=120)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="report_exports",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    parameters_json = models.JSONField(default=dict, blank=True)
    file = models.FileField(upload_to="reports/%Y/%m/%d", blank=True)

    class Meta:
        ordering = ["-created_at"]

# Create your models here.
