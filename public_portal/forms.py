from django import forms


class VerificationSearchForm(forms.Form):
    lookup_value = forms.CharField(max_length=128, label="Mã tra cứu / mã chứng chỉ / QR slug")
