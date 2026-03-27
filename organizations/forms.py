from django import forms

from organizations.models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            "code",
            "name",
            "description",
            "organization_type",
            "parent",
            "contact_email",
            "address",
            "is_validator",
            "can_write_ledger",
            "can_approve",
            "public_visible",
            "active",
        ]
