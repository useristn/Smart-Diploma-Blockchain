from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import OrganizationMembership, User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "full_name",
            "role",
            "primary_organization",
            "job_title",
            "phone",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "full_name", "job_title", "phone"]


class MembershipForm(forms.ModelForm):
    class Meta:
        model = OrganizationMembership
        fields = ["user", "organization", "role", "is_primary", "is_active"]
