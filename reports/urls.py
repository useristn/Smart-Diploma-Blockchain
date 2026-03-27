from django.urls import path

from reports.views import ReportExportCsvView, ReportExportPdfView, ReportSummaryTemplateView


app_name = "reports"

urlpatterns = [
    path("", ReportSummaryTemplateView.as_view(), name="summary"),
    path("xuat-csv/", ReportExportCsvView.as_view(), name="export_csv"),
    path("xuat-pdf/", ReportExportPdfView.as_view(), name="export_pdf"),
]
