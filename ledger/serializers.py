from rest_framework import serializers

from ledger.models import LedgerEvent


class LedgerEventSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor_user.username", read_only=True)
    actor_organization_name = serializers.CharField(source="actor_organization.name", read_only=True)

    class Meta:
        model = LedgerEvent
        fields = [
            "id",
            "sequence_no",
            "event_type",
            "entity_type",
            "entity_id",
            "actor_user",
            "actor_username",
            "actor_organization",
            "actor_organization_name",
            "payload_json",
            "previous_hash",
            "current_hash",
            "signature",
            "is_valid",
            "validation_notes",
            "created_at",
        ]
