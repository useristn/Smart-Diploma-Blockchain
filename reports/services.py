from io import StringIO, BytesIO
import csv
from datetime import datetime

from django.db import models

from credentials.models import Credential
from issuance.models import IssuanceRequest
from reports.models import ReportExport
from verification.models import VerificationLog


def build_report_summary():
    by_status = {
        row["current_status"]: row["total"]
        for row in Credential.objects.values("current_status")
        .order_by("current_status")
        .annotate(total=models.Count("id"))
    }
    by_type = {
        row["credential_type__name"]: row["total"]
        for row in Credential.objects.values("credential_type__name").annotate(total=models.Count("id"))
    }
    by_faculty = {
        (row["student__faculty__name"] or "N/A"): row["total"]
        for row in Credential.objects.values("student__faculty__name").annotate(total=models.Count("id"))
    }
    return {
        "credentials_total": Credential.objects.count(),
        "issuance_requests_total": IssuanceRequest.objects.count(),
        "verification_total": VerificationLog.objects.count(),
        "revoked_total": Credential.objects.filter(current_status="REVOKED").count(),
        "rejected_requests_total": IssuanceRequest.objects.filter(status="REJECTED").count(),
        "by_status": by_status,
        "by_type": by_type,
        "by_faculty": by_faculty,
    }


def export_reports(user=None):
    summary = build_report_summary()
    buffer = StringIO()
    writer = csv.writer(buffer)

    # Summary section
    writer.writerow(["=== TỔNG HỢP ==="])
    writer.writerow(["Chỉ số", "Giá trị"])
    writer.writerow(["Tổng chứng chỉ", summary["credentials_total"]])
    writer.writerow(["Tổng hồ sơ", summary["issuance_requests_total"]])
    writer.writerow(["Tổng lượt verify", summary["verification_total"]])
    writer.writerow(["Đã thu hồi", summary["revoked_total"]])
    writer.writerow(["Hồ sơ bị từ chối", summary["rejected_requests_total"]])
    writer.writerow([])

    # By status
    writer.writerow(["=== THEO TRẠNG THÁI ==="])
    writer.writerow(["Trạng thái", "Số lượng"])
    for status, count in summary["by_status"].items():
        writer.writerow([status, count])
    writer.writerow([])

    # By type
    writer.writerow(["=== THEO LOẠI ==="])
    writer.writerow(["Loại chứng chỉ", "Số lượng"])
    for ctype, count in summary["by_type"].items():
        writer.writerow([ctype, count])
    writer.writerow([])

    # By faculty
    writer.writerow(["=== THEO KHOA ==="])
    writer.writerow(["Khoa", "Số lượng"])
    for faculty, count in summary["by_faculty"].items():
        writer.writerow([faculty, count])
    writer.writerow([])

    # Detailed credentials list
    writer.writerow(["=== DANH SÁCH CHỨNG CHỈ CHI TIẾT ==="])
    writer.writerow([
        "Mã chứng chỉ", "Serial", "Loại", "Sinh viên", "Mã SV",
        "Khoa", "Trạng thái", "Ngày cấp", "Ngày phát hành", "Người ký",
    ])
    for cred in Credential.objects.select_related(
        "student", "credential_type", "student__faculty"
    ).order_by("-issued_at", "-created_at"):
        writer.writerow([
            cred.credential_code,
            cred.serial_number,
            cred.credential_type.name,
            cred.student.full_name,
            cred.student.student_code,
            getattr(cred.student.faculty, "name", "N/A"),
            cred.current_status,
            cred.issued_at.strftime("%d/%m/%Y %H:%M") if cred.issued_at else "",
            cred.published_at.strftime("%d/%m/%Y %H:%M") if cred.published_at else "",
            cred.signer_name or "",
        ])

    report = ReportExport.objects.create(
        report_type="summary",
        requested_by=user,
        parameters_json=summary,
    )
    return report, buffer.getvalue()


def export_pdf_report(user=None):
    """Generate a PDF summary report using reportlab."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
    )

    summary = build_report_summary()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"], fontSize=20,
        textColor=colors.HexColor("#0f172a"), spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle", parent=styles["Normal"], fontSize=10,
        textColor=colors.HexColor("#64748b"), spaceAfter=16,
    )
    section_style = ParagraphStyle(
        "SectionHeader", parent=styles["Heading2"], fontSize=13,
        textColor=colors.HexColor("#1d4ed8"), spaceBefore=16, spaceAfter=8,
    )

    elements = []

    # Title
    elements.append(Paragraph("Báo cáo tổng hợp chứng chỉ số", title_style))
    elements.append(Paragraph(
        f"Demo Blockchain Credential Ledger · Xuất lúc {datetime.now():%d/%m/%Y %H:%M}",
        subtitle_style,
    ))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))
    elements.append(Spacer(1, 10))

    # Summary KPIs table
    elements.append(Paragraph("Tổng hợp số liệu", section_style))
    kpi_data = [
        ["Chỉ số", "Giá trị"],
        ["Tổng chứng chỉ", str(summary["credentials_total"])],
        ["Tổng hồ sơ cấp phát", str(summary["issuance_requests_total"])],
        ["Tổng lượt xác thực", str(summary["verification_total"])],
        ["Chứng chỉ đã thu hồi", str(summary["revoked_total"])],
        ["Hồ sơ bị từ chối", str(summary["rejected_requests_total"])],
    ]
    kpi_table = Table(kpi_data, colWidths=[120 * mm, 40 * mm])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 10))

    # By status
    if summary["by_status"]:
        elements.append(Paragraph("Theo trạng thái", section_style))
        status_data = [["Trạng thái", "Số lượng"]]
        for status, count in summary["by_status"].items():
            status_data.append([status, str(count)])
        status_table = Table(status_data, colWidths=[120 * mm, 40 * mm])
        status_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        elements.append(status_table)
        elements.append(Spacer(1, 10))

    # By type
    if summary["by_type"]:
        elements.append(Paragraph("Theo loại chứng chỉ", section_style))
        type_data = [["Loại", "Số lượng"]]
        for ctype, count in summary["by_type"].items():
            type_data.append([ctype or "N/A", str(count)])
        type_table = Table(type_data, colWidths=[120 * mm, 40 * mm])
        type_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        elements.append(type_table)
        elements.append(Spacer(1, 10))

    # By faculty
    if summary["by_faculty"]:
        elements.append(Paragraph("Theo khoa", section_style))
        fac_data = [["Khoa", "Số lượng"]]
        for fac, count in summary["by_faculty"].items():
            fac_data.append([fac or "N/A", str(count)])
        fac_table = Table(fac_data, colWidths=[120 * mm, 40 * mm])
        fac_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        elements.append(fac_table)

    # Footer
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94a3b8")))
    elements.append(Paragraph(
        "Tài liệu được tạo tự động bởi hệ thống Demo Blockchain Credential Ledger.",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#94a3b8")),
    ))

    doc.build(elements)

    report = ReportExport.objects.create(
        report_type="summary_pdf",
        requested_by=user,
        parameters_json=summary,
    )
    return report, buffer.getvalue()
