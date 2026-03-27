from rest_framework import serializers

from accounts.models import OrganizationMembership, User


class UserSerializer(serializers.ModelSerializer):
    primary_organization_name = serializers.CharField(
        source="primary_organization.name",
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "role",
            "job_title",
            "phone",
            "primary_organization",
            "primary_organization_name",
            "is_active",
        ]


class MembershipSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = OrganizationMembership
        fields = [
            "id",
            "user",
            "user_name",
            "organization",
            "organization_name",
            "role",
            "is_primary",
            "is_active",
        ]
