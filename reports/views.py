from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from reports.services import build_report_summary, export_reports, export_pdf_report


class ReportSummaryTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "reports/summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["summary"] = build_report_summary()
        return context


class ReportExportCsvView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        _, csv_content = export_reports(user=request.user)
        response = HttpResponse(csv_content, content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="credential-report-summary.csv"'
        return response


class ReportExportPdfView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        _, pdf_content = export_pdf_report(user=request.user)
        response = HttpResponse(pdf_content, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="credential-report-summary.pdf"'
        return response


class ReportSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(build_report_summary())
