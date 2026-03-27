from django.conf import settings
from django.db import models

from core.choices import (
    ApprovalStatus,
    ApprovalStepType,
    IssuanceRequestStatus,
)
from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class IssuanceRequest(UUIDPrimaryKeyModel, TimeStampedModel):
    request_code = models.CharField(max_length=32, unique=True)
    student = models.ForeignKey(
        "students.Student",
        related_name="issuance_requests",
        on_delete=models.CASCADE,
    )
    credential_type = models.ForeignKey(
        "credentials.CredentialType",
        related_name="issuance_requests",
        on_delete=models.PROTECT,
    )
    template = models.ForeignKey(
        "credentials.CredentialTemplate",
        related_name="issuance_requests",
        on_delete=models.PROTECT,
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="requested_issuance_requests",
        on_delete=models.PROTECT,
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=24,
        choices=IssuanceRequestStatus.choices,
        default=IssuanceRequestStatus.SUBMITTED,
    )
    notes = models.TextField(blank=True)
    evaluation_summary_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return self.request_code


class ApprovalStep(UUIDPrimaryKeyModel, TimeStampedModel):
    request = models.ForeignKey(
        IssuanceRequest,
        related_name="approval_steps",
        on_delete=models.CASCADE,
    )
    step_type = models.CharField(max_length=24, choices=ApprovalStepType.choices)
    assigned_to_role = models.CharField(max_length=32)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="approval_steps",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=16,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ("request", "step_type")


class BatchIssuance(UUIDPrimaryKeyModel, TimeStampedModel):
    """Groups multiple IssuanceRequests, computes a Merkle root over their
    credential payload hashes, and anchors the batch to the ledger."""

    batch_code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requests = models.ManyToManyField(
        IssuanceRequest,
        related_name="batches",
        blank=True,
    )
    merkle_root = models.CharField(max_length=128, blank=True)
    committed_at = models.DateTimeField(null=True, blank=True)
    committed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="committed_batches",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.batch_code} - {self.name}"

    @property
    def is_committed(self):
        return bool(self.committed_at)
