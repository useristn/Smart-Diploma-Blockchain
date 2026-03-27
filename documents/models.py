from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class DocumentAttachment(UUIDPrimaryKeyModel, TimeStampedModel):
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=64)
    file = models.FileField(upload_to="attachments/%Y/%m/%d")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="uploaded_documents",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.entity_type}:{self.entity_id}"

# Create your models here.
