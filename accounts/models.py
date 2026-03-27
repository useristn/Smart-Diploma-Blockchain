from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.choices import UserRole
from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class User(AbstractUser, UUIDPrimaryKeyModel, TimeStampedModel):
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=32,
        choices=UserRole.choices,
        default=UserRole.ORGANIZATION_STAFF,
    )
    primary_organization = models.ForeignKey(
        "organizations.Organization",
        related_name="primary_users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    job_title = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["username"]

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.get_full_name() or self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.username


class OrganizationMembership(UUIDPrimaryKeyModel, TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="memberships",
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        related_name="memberships",
        on_delete=models.CASCADE,
    )
    role = models.CharField(max_length=32, choices=UserRole.choices)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "organization", "role")
        ordering = ["organization__name", "user__username"]

    def __str__(self):
        return f"{self.user} @ {self.organization} ({self.role})"

# Create your models here.
