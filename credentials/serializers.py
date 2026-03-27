from rest_framework import serializers

from credentials.models import Credential, CredentialType


class CredentialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialType
        fields = [
            "id",
            "code",
            "name",
            "description",
            "default_validity_type",
            "public_fields_json",
            "allow_public_pdf",
            "active",
        ]


class CredentialSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    credential_type_name = serializers.CharField(source="credential_type.name", read_only=True)
    issuer_name = serializers.CharField(source="issuer_organization.name", read_only=True)

    class Meta:
        model = Credential
        fields = [
            "id",
            "credential_code",
            "serial_number",
            "verification_code",
            "public_slug",
            "student",
            "student_name",
            "credential_type",
            "credential_type_name",
            "issuer_organization",
            "issuer_name",
            "current_status",
            "issued_at",
            "published_at",
            "revoked_at",
            "payload_hash",
            "pdf_hash",
            "ledger_anchor_hash",
            "notes",
        ]
