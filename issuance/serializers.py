from rest_framework import serializers

from issuance.models import ApprovalStep, IssuanceRequest


class IssuanceRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    credential_type_name = serializers.CharField(source="credential_type.name", read_only=True)

    class Meta:
        model = IssuanceRequest
        fields = [
            "id",
            "request_code",
            "student",
            "student_name",
            "credential_type",
            "credential_type_name",
            "template",
            "requested_by",
            "requested_at",
            "status",
            "notes",
            "evaluation_summary_json",
        ]


class ApprovalStepSerializer(serializers.ModelSerializer):
    approved_by_name = serializers.CharField(source="approved_by.full_name", read_only=True)

    class Meta:
        model = ApprovalStep
        fields = [
            "id",
            "request",
            "step_type",
            "assigned_to_role",
            "approved_by",
            "approved_by_name",
            "approved_at",
            "status",
            "note",
        ]
