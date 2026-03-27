from django.db import models

from core.choices import OrganizationType
from core.models import NamedModel


class Organization(NamedModel):
    organization_type = models.CharField(
        max_length=32,
        choices=OrganizationType.choices,
        default=OrganizationType.UNIVERSITY,
    )
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contact_email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    metadata_json = models.JSONField(default=dict, blank=True)
    is_validator = models.BooleanField(default=True)
    can_write_ledger = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
    public_visible = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

# Create your models here.
