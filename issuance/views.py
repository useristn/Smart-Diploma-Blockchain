from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from rest_framework import permissions, viewsets

from accounts.permissions import RoleRequiredMixin
from core.choices import UserRole
from credentials.services import issue_credential_from_request
from issuance.forms import ApprovalActionForm, BatchIssuanceForm, IssuanceRequestForm
from issuance.models import ApprovalStep, BatchIssuance, IssuanceRequest
from issuance.serializers import ApprovalStepSerializer, IssuanceRequestSerializer
from issuance.services import (
    commit_batch_issuance,
    create_batch_issuance,
    create_issuance_request,
    get_merkle_proof_for_credential,
    run_approval_step,
)
from policy_engine.services import evaluate_eligibility_rules


class IssuanceRequestListView(LoginRequiredMixin, ListView):
    model = IssuanceRequest
    template_name = "issuance/list.html"
    context_object_name = "requests"

    def get_queryset(self):
        return IssuanceRequest.objects.select_related(
            "student", "credential_type", "template", "requested_by"
        )


class IssuanceRequestCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = (
        UserRole.SYSTEM_ADMIN,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.FACULTY_ADMIN,
        UserRole.DEPARTMENT_OFFICER,
    )
    model = IssuanceRequest
    form_class = IssuanceRequestForm
    template_name = "issuance/form.html"
    success_url = reverse_lazy("issuance:list")

    def form_valid(self, form):
        create_issuance_request(
            student=form.cleaned_data["student"],
            credential_type=form.cleaned_data["credential_type"],
            template=form.cleaned_data["template"],
            requested_by=self.request.user,
            notes=form.cleaned_data.get("notes", ""),
        )
        messages.success(self.request, "Đã tạo hồ sơ cấp phát.")
        return redirect(self.success_url)
        return redirect(self.success_url)


class IssuanceRequestDetailView(LoginRequiredMixin, DetailView):
    model = IssuanceRequest
    template_name = "issuance/detail.html"
    context_object_name = "issuance_request"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["approval_form"] = ApprovalActionForm()
        context["approval_steps"] = self.object.approval_steps.select_related("approved_by")
        context["evaluations"] = self.object.policy_evaluations.select_related("rule")
        return context


class EvaluateEligibilityView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (
        UserRole.SYSTEM_ADMIN,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.FACULTY_ADMIN,
        UserRole.DEPARTMENT_OFFICER,
    )

    def post(self, request, pk):
        request_obj = get_object_or_404(IssuanceRequest, pk=pk)
        evaluate_eligibility_rules(request_obj, actor_user=request.user)
        messages.success(request, "Đã chạy đánh giá policy rules.")
        return redirect("issuance:detail", pk=pk)


class ApprovalStepActionView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (
        UserRole.SYSTEM_ADMIN,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.FACULTY_ADMIN,
        UserRole.EXAMINATION_OFFICER,
        UserRole.AUDITOR,
        UserRole.REGISTRAR,
    )

    def post(self, request, pk, step_type, action):
        request_obj = get_object_or_404(IssuanceRequest, pk=pk)
        approved = action == "approve"
        note = request.POST.get("note", "")
        run_approval_step(request_obj, step_type, request.user, approved, note)
        messages.success(request, "Đã cập nhật bước phê duyệt.")
        return redirect("issuance:detail", pk=pk)


class IssueCredentialView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (
        UserRole.SYSTEM_ADMIN,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.REGISTRAR,
    )

    def post(self, request, pk):
        request_obj = get_object_or_404(IssuanceRequest, pk=pk)
        credential = issue_credential_from_request(request_obj, actor_user=request.user)
        messages.success(request, f"Đã sinh chứng chỉ {credential.credential_code}.")
        return redirect("credentials:detail", pk=credential.pk)


class IssuanceRequestViewSet(viewsets.ModelViewSet):
    queryset = IssuanceRequest.objects.select_related("student", "credential_type", "template").all()
    serializer_class = IssuanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApprovalStepViewSet(viewsets.ModelViewSet):
    queryset = ApprovalStep.objects.select_related("request", "approved_by").all()
    serializer_class = ApprovalStepSerializer
    permission_classes = [permissions.IsAuthenticated]


# ──────────────────────────────────────────────────────────────────────────────
# Batch Issuance (Merkle) views
# ──────────────────────────────────────────────────────────────────────────────

class BatchIssuanceListView(LoginRequiredMixin, ListView):
    model = BatchIssuance
    template_name = "issuance/batch_list.html"
    context_object_name = "batches"

    def get_queryset(self):
        return BatchIssuance.objects.prefetch_related("requests").all()


class BatchIssuanceCreateView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (
        UserRole.SYSTEM_ADMIN,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.REGISTRAR,
    )
    template_name = "issuance/batch_form.html"

    def get(self, request):
        from django.shortcuts import render
        form = BatchIssuanceForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        from django.shortcuts import render
        form = BatchIssuanceForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        batch = create_batch_issuance(
            name=form.cleaned_data["name"],
            description=form.cleaned_data.get("description", ""),
            request_ids=[r.id for r in form.cleaned_data["requests"]],
            actor_user=request.user,
        )
        messages.success(request, f"Đã tạo batch {batch.batch_code}.")
        return redirect("issuance:batch_detail", pk=batch.pk)


class BatchIssuanceDetailView(LoginRequiredMixin, DetailView):
    model = BatchIssuance
    template_name = "issuance/batch_detail.html"
    context_object_name = "batch"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batch = self.object
        from credentials.models import Credential
        credentials = list(
            Credential.objects.filter(
                issuance_request__in=batch.requests.all()
            ).select_related("student", "credential_type")
        )
        context["credentials"] = credentials
        if batch.is_committed:
            hashes = sorted([c.payload_hash for c in credentials if c.payload_hash])
            leaves = []
            for c in credentials:
                if c.payload_hash:
                    proof = get_merkle_proof_for_credential(batch, str(c.id))
                    leaves.append({
                        "credential": c,
                        "hash": c.payload_hash,
                        "proof": proof.get("proof", []),
                    })
            context["merkle_leaves"] = leaves
        return context


class CommitBatchView(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = (
        UserRole.SYSTEM_ADMIN,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.REGISTRAR,
    )

    def post(self, request, pk):
        batch = get_object_or_404(BatchIssuance, pk=pk)
        try:
            commit_batch_issuance(batch, request.user)
            messages.success(
                request,
                f"Batch {batch.batch_code} đã được commit vào ledger. "
                f"Merkle root: {batch.merkle_root[:16]}…",
            )
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect("issuance:batch_detail", pk=pk)
