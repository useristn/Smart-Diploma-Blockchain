from django.contrib import admin

from credentials.models import (
    Credential,
    CredentialTemplate,
    CredentialType,
    CredentialVersion,
    RevocationRecord,
    SignatureRecord,
    SigningKey,
)


@admin.register(CredentialType)
class CredentialTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "allow_public_pdf", "active")


@admin.register(CredentialTemplate)
class CredentialTemplateAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "credential_type", "version", "active")


@admin.register(SigningKey)
class SigningKeyAdmin(admin.ModelAdmin):
    list_display = ("organization", "key_name", "algorithm", "active", "created_at")


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ("credential_code", "student", "credential_type", "current_status", "issued_at", "published_at")
    list_filter = ("current_status", "credential_type")
    search_fields = ("credential_code", "serial_number", "verification_code", "student__full_name")


@admin.register(CredentialVersion)
class CredentialVersionAdmin(admin.ModelAdmin):
    list_display = ("credential", "version_no", "created_at")


@admin.register(SignatureRecord)
class SignatureRecordAdmin(admin.ModelAdmin):
    list_display = ("credential", "signing_key", "signature_algorithm", "verified", "signed_at")


@admin.register(RevocationRecord)
class RevocationRecordAdmin(admin.ModelAdmin):
    list_display = ("credential", "decision_number", "ordered_by", "ordered_at")

# Register your models here.
