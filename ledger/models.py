from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class LedgerEvent(UUIDPrimaryKeyModel, TimeStampedModel):
    sequence_no = models.PositiveIntegerField(unique=True)
    event_type = models.CharField(max_length=64)
    entity_type = models.CharField(max_length=64)
    entity_id = models.CharField(max_length=64)
    actor_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="ledger_events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    actor_organization = models.ForeignKey(
        "organizations.Organization",
        related_name="ledger_events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    payload_json = models.JSONField(default=dict, blank=True)
    previous_hash = models.CharField(max_length=128, blank=True)
    current_hash = models.CharField(max_length=128, unique=True)
    signature = models.TextField(blank=True)
    is_valid = models.BooleanField(default=True)
    validation_notes = models.TextField(blank=True)
    block_no = models.PositiveIntegerField(null=True, blank=True)
    batch_no = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["sequence_no"]

    def __str__(self):
        return f"{self.sequence_no} - {self.event_type}"

# Create your models here.
