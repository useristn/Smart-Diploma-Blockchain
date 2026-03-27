from django.conf import settings
from django.db import models

from core.choices import CredentialStatus
from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class CredentialType(UUIDPrimaryKeyModel, TimeStampedModel):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    default_validity_type = models.CharField(max_length=120, blank=True)
    public_fields_json = models.JSONField(default=list, blank=True)
    allow_public_pdf = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.name


class CredentialTemplate(UUIDPrimaryKeyModel, TimeStampedModel):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255)
    credential_type = models.ForeignKey(
        CredentialType,
        related_name="templates",
        on_delete=models.CASCADE,
    )
    version = models.CharField(max_length=32, default="1.0")
    template_config_json = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["credential_type__code", "code"]

    def __str__(self):
        return f"{self.name} v{self.version}"


class SigningKey(UUIDPrimaryKeyModel, TimeStampedModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        related_name="signing_keys",
        on_delete=models.CASCADE,
    )
    key_name = models.CharField(max_length=255)
    algorithm = models.CharField(max_length=32, default="RSA")
    public_key_pem = models.TextField()
    private_key_reference = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["organization__name", "key_name"]

    def __str__(self):
        return f"{self.organization.name} - {self.key_name}"


class Credential(UUIDPrimaryKeyModel, TimeStampedModel):
    credential_code = models.CharField(max_length=32, unique=True)
    serial_number = models.CharField(max_length=32, unique=True)
    verification_code = models.CharField(max_length=32, unique=True)
    public_slug = models.SlugField(max_length=64, unique=True)
    issuance_request = models.OneToOneField(
        "issuance.IssuanceRequest",
        related_name="credential",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    student = models.ForeignKey(
        "students.Student",
        related_name="credentials",
        on_delete=models.PROTECT,
    )
    credential_type = models.ForeignKey(
        CredentialType,
        related_name="credentials",
        on_delete=models.PROTECT,
    )
    template = models.ForeignKey(
        CredentialTemplate,
        related_name="credentials",
        on_delete=models.PROTECT,
    )
    issuer_organization = models.ForeignKey(
        "organizations.Organization",
        related_name="issued_credentials",
        on_delete=models.PROTECT,
    )
    current_status = models.CharField(
        max_length=16,
        choices=CredentialStatus.choices,
        default=CredentialStatus.DRAFT,
    )
    issued_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    superseded_by = models.ForeignKey(
        "self",
        related_name="superseded_credentials",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    payload_json = models.JSONField(default=dict, blank=True)
    payload_hash = models.CharField(max_length=128, blank=True)
    pdf_file = models.FileField(upload_to="credentials/pdfs/%Y/%m/%d", blank=True)
    pdf_hash = models.CharField(max_length=128, blank=True)
    qr_image = models.ImageField(upload_to="credentials/qr/%Y/%m/%d", blank=True)
    signature_value = models.TextField(blank=True)
    signer_name = models.CharField(max_length=255, blank=True)
    signer_title = models.CharField(max_length=255, blank=True)
    ledger_anchor_hash = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-issued_at", "-created_at"]

    def __str__(self):
        return self.credential_code


class CredentialVersion(UUIDPrimaryKeyModel, TimeStampedModel):
    credential = models.ForeignKey(
        Credential,
        related_name="versions",
        on_delete=models.CASCADE,
    )
    version_no = models.PositiveIntegerField()
    payload_json = models.JSONField(default=dict, blank=True)
    payload_hash = models.CharField(max_length=128)
    pdf_file = models.FileField(upload_to="credentials/versions/%Y/%m/%d", blank=True)
    pdf_hash = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["-version_no"]
        unique_together = ("credential", "version_no")


class SignatureRecord(UUIDPrimaryKeyModel, TimeStampedModel):
    credential = models.ForeignKey(
        Credential,
        related_name="signature_records",
        on_delete=models.CASCADE,
    )
    signing_key = models.ForeignKey(
        SigningKey,
        related_name="signature_records",
        on_delete=models.PROTECT,
    )
    signature_algorithm = models.CharField(max_length=32, default="RSA")
    signed_payload_hash = models.CharField(max_length=128)
    signature_value = models.TextField()
    verified = models.BooleanField(default=False)
    signed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-signed_at"]


class RevocationRecord(UUIDPrimaryKeyModel, TimeStampedModel):
    credential = models.ForeignKey(
        Credential,
        related_name="revocation_records",
        on_delete=models.CASCADE,
    )
    reason = models.TextField()
    decision_number = models.CharField(max_length=64)
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="ordered_revocations",
        on_delete=models.PROTECT,
    )
    ordered_at = models.DateTimeField(auto_now_add=True)
    public_note = models.TextField(blank=True)
    attachment = models.FileField(upload_to="credentials/revocations/%Y/%m/%d", blank=True)

    class Meta:
        ordering = ["-ordered_at"]

# Create your models here.
