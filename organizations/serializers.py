from rest_framework import serializers

from organizations.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source="parent.name", read_only=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "code",
            "name",
            "description",
            "organization_type",
            "parent",
            "parent_name",
            "contact_email",
            "address",
            "is_validator",
            "can_write_ledger",
            "can_approve",
            "public_visible",
            "active",
        ]
