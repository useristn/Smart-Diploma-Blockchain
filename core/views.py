from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
import json


class HomeRedirectView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return redirect("accounts:login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get(self, request, *args, **kwargs):
        from core.choices import UserRole
        if request.user.role == UserRole.STUDENT:
            return redirect("students:portal")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        from credentials.models import Credential
        from django.db.models import Count
        from datetime import timedelta
        from django.utils import timezone
        from issuance.models import IssuanceRequest
        from ledger.services import verify_ledger_chain
        from organizations.models import Organization
        from students.models import Student
        from verification.models import VerificationLog

        context = super().get_context_data(**kwargs)
        recent_requests = IssuanceRequest.objects.select_related(
            "student", "credential_type"
        ).order_by("-created_at")[:5]
        recent_credentials = Credential.objects.select_related(
            "student", "credential_type"
        ).order_by("-issued_at", "-created_at")[:5]
        pending_requests = IssuanceRequest.objects.filter(
            status__in=["SUBMITTED", "UNDER_REVIEW", "ACADEMIC_ELIGIBLE"]
        ).count()
        integrity_report = verify_ledger_chain(limit=100)

        # ── Chart data ──────────────────────────────────────────────────────
        status_qs = (
            Credential.objects.values("current_status")
            .annotate(total=Count("id"))
            .order_by("current_status")
        )
        STATUS_COLORS = {
            "DRAFT":      "#94a3b8",
            "ISSUED":     "#60a5fa",
            "SIGNED":     "#a78bfa",
            "PUBLISHED":  "#34d399",
            "SUSPENDED":  "#fbbf24",
            "REVOKED":    "#f87171",
            "SUPERSEDED": "#fb923c",
        }
        STATUS_LABELS = {
            "DRAFT":      "Nháp",
            "ISSUED":     "Đã cấp",
            "SIGNED":     "Đã ký",
            "PUBLISHED":  "Đã công bố",
            "SUSPENDED":  "Tạm đình chỉ",
            "REVOKED":    "Thu hồi",
            "SUPERSEDED": "Thay thế",
        }
        chart_status_labels = [STATUS_LABELS.get(r["current_status"], r["current_status"]) for r in status_qs]
        chart_status_data = [r["total"] for r in status_qs]
        chart_status_colors = [STATUS_COLORS.get(r["current_status"], "#94a3b8") for r in status_qs]

        today = timezone.now().date()
        fourteen_days_ago = today - timedelta(days=13)
        verif_labels = []
        verif_data = []
        for i in range(14):
            day = fourteen_days_ago + timedelta(days=i)
            verif_labels.append(day.strftime("%d/%m"))
            verif_data.append(
                VerificationLog.objects.filter(verified_at__date=day).count()
            )

        context.update(
            {
                "kpis": {
                    "organizations": Organization.objects.count(),
                    "students": Student.objects.count(),
                    "issuance_requests": IssuanceRequest.objects.count(),
                    "credentials": Credential.objects.count(),
                    "pending_requests": pending_requests,
                    "verification_logs": VerificationLog.objects.count(),
                },
                "recent_requests": recent_requests,
                "recent_credentials": recent_credentials,
                "integrity_report": integrity_report,
                # charts
                "chart_status_labels": json.dumps(chart_status_labels),
                "chart_status_data": json.dumps(chart_status_data),
                "chart_status_colors": json.dumps(chart_status_colors),
                "chart_verif_labels": json.dumps(verif_labels),
                "chart_verif_data": json.dumps(verif_data),
            }
        )
        return context

# Create your views here.
