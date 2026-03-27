from django import forms

from issuance.models import BatchIssuance, IssuanceRequest


class IssuanceRequestForm(forms.ModelForm):
    class Meta:
        model = IssuanceRequest
        fields = ["student", "credential_type", "template", "notes"]


class ApprovalActionForm(forms.Form):
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))


class BatchIssuanceForm(forms.ModelForm):
    requests = forms.ModelMultipleChoiceField(
        queryset=IssuanceRequest.objects.select_related("student", "credential_type"),
        widget=forms.CheckboxSelectMultiple,
        label="Hồ sơ cấp phát đưa vào batch",
        help_text="Chọn các hồ sơ đã được phê duyệt cuối (hoặc đã có credential).",
    )

    class Meta:
        model = BatchIssuance
        fields = ["name", "description", "requests"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
