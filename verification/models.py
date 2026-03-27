from django.db import models

from core.choices import VerificationMethod
from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class VerificationLog(UUIDPrimaryKeyModel, TimeStampedModel):
    credential = models.ForeignKey(
        "credentials.Credential",
        related_name="verification_logs",
        on_delete=models.CASCADE,
    )
    verification_method = models.CharField(
        max_length=24,
        choices=VerificationMethod.choices,
        default=VerificationMethod.CODE,
    )
    requester_ip = models.GenericIPAddressField(null=True, blank=True)
    requester_user_agent = models.CharField(max_length=255, blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=32)

    class Meta:
        ordering = ["-verified_at"]

# Create your models here.
