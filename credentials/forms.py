import json

from django import forms

from credentials.models import SigningKey


class SignCredentialForm(forms.Form):
    signing_key = forms.ModelChoiceField(queryset=SigningKey.objects.none())
    signer_title = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        organization = kwargs.pop("organization", None)
        super().__init__(*args, **kwargs)
        queryset = SigningKey.objects.filter(active=True)
        if organization is not None:
            queryset = queryset.filter(organization=organization)
        self.fields["signing_key"].queryset = queryset


class RevokeCredentialForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    decision_number = forms.CharField(max_length=64)
    public_note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))


class SupersedeCredentialForm(forms.Form):
    corrected_payload_json = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 8}),
        help_text="Nhập JSON payload chỉnh sửa.",
    )
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def clean_corrected_payload_json(self):
        raw = self.cleaned_data["corrected_payload_json"]
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise forms.ValidationError(f"JSON không hợp lệ: {exc}") from exc
