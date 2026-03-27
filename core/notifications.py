import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def _send_notification(subject, template_name, context, recipient_email):
    """Send an HTML email notification. Fails silently in dev mode."""
    if not recipient_email:
        logger.warning("No recipient email for notification: %s", subject)
        return False
    try:
        context.setdefault("site_url", getattr(settings, "SITE_BASE_URL", ""))
        context.setdefault("system_name", "Demo Blockchain Credential Ledger")
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=True,
        )
        logger.info("Notification sent to %s: %s", recipient_email, subject)
        return True
    except Exception:
        logger.exception("Failed to send notification to %s", recipient_email)
        return False


def send_credential_notification(credential, event_type):
    """Send email to student when credential status changes."""
    student = credential.student
    if not student.email:
        return

    template_map = {
        "issued": "emails/credential_issued.html",
        "published": "emails/credential_published.html",
        "revoked": "emails/credential_revoked.html",
    }
    subject_map = {
        "issued": f"Chứng chỉ {credential.credential_code} đã được tạo",
        "published": f"Chứng chỉ {credential.credential_code} đã được phát hành",
        "revoked": f"Chứng chỉ {credential.credential_code} đã bị thu hồi",
    }
    template = template_map.get(event_type)
    subject = subject_map.get(event_type)
    if not template:
        return

    _send_notification(
        subject=subject,
        template_name=template,
        context={
            "credential": credential,
            "student": student,
            "verification_url": f"{getattr(settings, 'SITE_BASE_URL', '')}/xac-thuc/tra-cuu/{credential.public_slug}/",
        },
        recipient_email=student.email,
    )


def send_approval_notification(request_obj, step, approved):
    """Send email to the requesting user when an approval step is completed."""
    user = request_obj.requested_by
    if not user or not user.email:
        return

    _send_notification(
        subject=f"Cập nhật phê duyệt hồ sơ {request_obj.request_code}",
        template_name="emails/approval_update.html",
        context={
            "request_obj": request_obj,
            "step": step,
            "approved": approved,
            "student": request_obj.student,
        },
        recipient_email=user.email,
    )
