from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from rest_framework import permissions, viewsets

from accounts.permissions import RoleRequiredMixin
from core.choices import UserRole
from credentials.forms import RevokeCredentialForm, SignCredentialForm, SupersedeCredentialForm
from credentials.models import Credential, CredentialType, SigningKey
from credentials.serializers import CredentialSerializer, CredentialTypeSerializer
from credentials.services import publish_credential, revoke_credential, sign_credential, supersede_credential


class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    template_name = "credentials/list.html"
    context_object_name = "credentials"

    def get_queryset(self):
        return Credential.objects.select_related(
            "student",
            "credential_type",
            "issuer_organization",
            "superseded_by",
        )


class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential
    template_name = "credentials/detail.html"
    context_object_name = "credential"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sign_form"] = SignCredentialForm(organization=self.object.issuer_organization)
        context["revoke_form"] = RevokeCredentialForm()
        context["supersede_form"] = SupersedeCredentialForm(
            initial={"corrected_payload_json": "{}"}
        )
        context["signature_records"] = self.object.signature_records.select_related("signing_key")
        context["versions"] = self.object.versions.all()
        context["revocations"] = self.object.revocation_records.all()
        return context


class SignCredentialView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.SIGNER, UserRole.REGISTRAR)

    def post(self, request, pk):
        credential = get_object_or_404(Credential, pk=pk)
        form = SignCredentialForm(request.POST, organization=credential.issuer_organization)
        if not form.is_valid():
            messages.error(request, "Không thể ký chứng chỉ. Vui lòng kiểm tra dữ liệu.")
            return redirect("credentials:detail", pk=pk)
        sign_credential(
            credential,
            signing_key=form.cleaned_data["signing_key"],
            actor_user=request.user,
            signer_title=form.cleaned_data["signer_title"],
        )
        messages.success(request, "Đã ký số chứng chỉ.")
        return redirect("credentials:detail", pk=pk)


class PublishCredentialView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.REGISTRAR)

    def post(self, request, pk):
        credential = get_object_or_404(Credential, pk=pk)
        publish_credential(credential, request.user)
        messages.success(request, "Đã publish chứng chỉ.")
        return redirect("credentials:detail", pk=pk)


class RevokeCredentialView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN, UserRole.REGISTRAR, UserRole.AUDITOR)

    def post(self, request, pk):
        credential = get_object_or_404(Credential, pk=pk)
        form = RevokeCredentialForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Biểu mẫu thu hồi chưa hợp lệ.")
            return redirect("credentials:detail", pk=pk)
        revoke_credential(
            credential,
            actor_user=request.user,
            reason=form.cleaned_data["reason"],
            decision_number=form.cleaned_data["decision_number"],
            public_note=form.cleaned_data["public_note"],
        )
        messages.success(request, "Đã thu hồi chứng chỉ.")
        return redirect("credentials:detail", pk=pk)


class SupersedeCredentialView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN, UserRole.REGISTRAR)

    def post(self, request, pk):
        credential = get_object_or_404(Credential, pk=pk)
        form = SupersedeCredentialForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Dữ liệu supersede không hợp lệ.")
            return redirect("credentials:detail", pk=pk)
        new_credential = supersede_credential(
            credential,
            actor_user=request.user,
            corrected_payload_updates=form.cleaned_data["corrected_payload_json"],
            notes=form.cleaned_data["notes"],
        )
        messages.success(
            request,
            f"Đã tạo bản thay thế {new_credential.credential_code}.",
        )
        return redirect("credentials:detail", pk=new_credential.pk)


class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.select_related("student", "credential_type", "issuer_organization").all()
    serializer_class = CredentialSerializer
    permission_classes = [permissions.IsAuthenticated]


class CredentialTypeViewSet(viewsets.ModelViewSet):
    queryset = CredentialType.objects.all()
    serializer_class = CredentialTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
