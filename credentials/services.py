from io import BytesIO
from pathlib import Path

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.template.defaultfilters import slugify
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from audit.services import log_action
from core.choices import CredentialStatus, IssuanceRequestStatus, LedgerEventType, UserRole
from core.notifications import send_credential_notification
from core.signing import sign_message, verify_message
from core.utils import canonicalize_json, generate_random_code, sha256_digest
from credentials.models import (
    Credential,
    CredentialVersion,
    RevocationRecord,
    SignatureRecord,
    SigningKey,
)
from issuance.services import is_final_approved
from ledger.services import commit_ledger_event


def compute_payload_hash(payload) -> str:
    return sha256_digest(canonicalize_json(payload))


def compute_pdf_hash(file_or_path) -> str:
    if hasattr(file_or_path, "read"):
        file_or_path.seek(0)
        data = file_or_path.read()
        file_or_path.seek(0)
        return sha256_digest(data)
    return sha256_digest(Path(file_or_path).read_bytes())


def generate_credential_payload(request_obj):
    student = request_obj.student
    program = student.academic_program
    return {
        "request_code": request_obj.request_code,
        "credential_type": request_obj.credential_type.name,
        "student": {
            "student_code": student.student_code,
            "full_name": student.full_name,
            "email": student.email,
            "cohort": student.cohort,
        },
        "program": {
            "code": program.code,
            "name": program.name,
            "degree_type": program.degree_type,
            "min_gpa": str(program.min_gpa),
            "required_credits": program.total_required_credits,
        },
        "academic_result": {
            "credits_completed": student.credits_completed,
            "gpa": str(student.gpa),
            "finance_hold": student.finance_hold,
            "discipline_hold": student.discipline_hold,
        },
        "issued_at": timezone.now().isoformat(),
    }


def _build_verification_url(credential) -> str:
    base_url = getattr(settings, "SITE_BASE_URL", "http://127.0.0.1:8000")
    return f"{base_url}/xac-thuc/tra-cuu/{credential.public_slug}/"


def generate_qr_code(credential):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(_build_verification_url(credential))
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    filename = f"{credential.credential_code.lower()}-qr.png"
    credential.qr_image.save(filename, ContentFile(buffer.getvalue()), save=False)
    return credential.qr_image


def render_credential_pdf(credential):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFillColor(colors.HexColor("#0f172a"))
    pdf.setStrokeColor(colors.HexColor("#1d4ed8"))
    pdf.rect(18 * mm, 18 * mm, width - 36 * mm, height - 36 * mm, stroke=1, fill=0)

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(width / 2, height - 40 * mm, "DEMO BLOCKCHAIN UNIVERSITY")
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, height - 48 * mm, "Digital Credential Ledger")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, height - 68 * mm, credential.credential_type.name.upper())
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2, height - 82 * mm, "This certifies that")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width / 2, height - 96 * mm, credential.student.full_name)

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        width / 2,
        height - 110 * mm,
        f"Student code: {credential.student.student_code} | Program: {credential.student.academic_program.name}",
    )
    pdf.drawCentredString(
        width / 2,
        height - 120 * mm,
        f"Credential code: {credential.credential_code} | Serial: {credential.serial_number}",
    )
    pdf.drawCentredString(
        width / 2,
        height - 130 * mm,
        f"Verification code: {credential.verification_code}",
    )

    pdf.setFont("Helvetica", 10)
    pdf.drawString(30 * mm, 55 * mm, f"Payload hash: {credential.payload_hash[:32]}...")
    pdf.drawString(30 * mm, 47 * mm, f"Issued by: {credential.issuer_organization.name}")
    pdf.drawString(30 * mm, 39 * mm, f"Issued at: {credential.issued_at:%d/%m/%Y %H:%M}")
    pdf.drawString(30 * mm, 31 * mm, f"Signer: {credential.signer_name or 'Pending signer'}")
    pdf.drawString(30 * mm, 23 * mm, _build_verification_url(credential))

    if credential.qr_image:
        pdf.drawImage(
            credential.qr_image.path,
            width - 60 * mm,
            22 * mm,
            width=28 * mm,
            height=28 * mm,
            preserveAspectRatio=True,
            mask="auto",
        )

    pdf.showPage()
    pdf.save()
    filename = f"{credential.credential_code.lower()}.pdf"
    credential.pdf_file.save(filename, ContentFile(buffer.getvalue()), save=False)
    return credential.pdf_file


def _signature_message_values(payload_hash: str, pdf_hash: str, credential_code: str) -> str:
    return canonicalize_json(
        {
            "credential_code": credential_code,
            "payload_hash": payload_hash,
            "pdf_hash": pdf_hash,
        }
    )


def _deep_merge(base: dict, updates: dict) -> dict:
    merged = dict(base)
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


@transaction.atomic
def issue_credential_from_request(request_obj, actor_user):
    if not is_final_approved(request_obj):
        raise ValueError("Ho so chua duoc phe duyet cuoi.")
    if hasattr(request_obj, "credential"):
        return request_obj.credential

    credential = Credential.objects.create(
        credential_code=generate_random_code("CRD", 8),
        serial_number=generate_random_code("SER", 8),
        verification_code=generate_random_code("VER", 8),
        public_slug=slugify(f"{request_obj.student.student_code}-{generate_random_code('PUB', 6)}"),
        issuance_request=request_obj,
        student=request_obj.student,
        credential_type=request_obj.credential_type,
        template=request_obj.template,
        issuer_organization=actor_user.primary_organization or request_obj.student.faculty,
        current_status=CredentialStatus.ISSUED,
        issued_at=timezone.now(),
        payload_json=generate_credential_payload(request_obj),
    )
    credential.payload_hash = compute_payload_hash(credential.payload_json)

    generate_qr_code(credential)
    render_credential_pdf(credential)
    credential.pdf_hash = compute_pdf_hash(credential.pdf_file.path)
    credential.save()

    CredentialVersion.objects.create(
        credential=credential,
        version_no=1,
        payload_json=credential.payload_json,
        payload_hash=credential.payload_hash,
        pdf_file=credential.pdf_file,
        pdf_hash=credential.pdf_hash,
    )

    event = commit_ledger_event(
        event_type=LedgerEventType.CREDENTIAL_ISSUED,
        entity_type="Credential",
        entity_id=credential.id,
        actor_user=actor_user,
        actor_organization=credential.issuer_organization,
        payload_json={
            "credential_code": credential.credential_code,
            "student_code": credential.student.student_code,
            "payload_hash": credential.payload_hash,
        },
    )
    commit_ledger_event(
        event_type=LedgerEventType.PDF_RENDERED,
        entity_type="Credential",
        entity_id=credential.id,
        actor_user=actor_user,
        actor_organization=credential.issuer_organization,
        payload_json={"pdf_hash": credential.pdf_hash, "pdf_file": credential.pdf_file.name},
    )
    credential.ledger_anchor_hash = event.current_hash
    credential.save(update_fields=["ledger_anchor_hash", "updated_at"])
    log_action(
        actor_user,
        action="credential.issued",
        object_type="Credential",
        object_id=credential.id,
        metadata={"credential_code": credential.credential_code},
    )
    send_credential_notification(credential, "issued")
    return credential


@transaction.atomic
def sign_credential(credential, signing_key: SigningKey, actor_user, signer_title=""):
    if credential.issuance_request and not is_final_approved(credential.issuance_request):
        raise ValueError("Khong the ky khi ho so chua duoc phe duyet cuoi.")
    message = _signature_message_values(
        credential.payload_hash,
        credential.pdf_hash,
        credential.credential_code,
    )
    signature = sign_message(signing_key.private_key_reference, message)
    verified = verify_message(signing_key.public_key_pem, message, signature)

    credential.signature_value = signature
    credential.signer_name = actor_user.full_name or actor_user.username
    credential.signer_title = signer_title or actor_user.job_title or "Certificate Signer"
    credential.current_status = CredentialStatus.SIGNED
    credential.save(
        update_fields=[
            "signature_value",
            "signer_name",
            "signer_title",
            "current_status",
            "updated_at",
        ]
    )
    SignatureRecord.objects.create(
        credential=credential,
        signing_key=signing_key,
        signature_algorithm=signing_key.algorithm,
        signed_payload_hash=credential.payload_hash,
        signature_value=signature,
        verified=verified,
    )
    if credential.issuance_request:
        credential.issuance_request.status = IssuanceRequestStatus.SIGNED
        credential.issuance_request.save(update_fields=["status", "updated_at"])

    event = commit_ledger_event(
        event_type=LedgerEventType.CREDENTIAL_SIGNED,
        entity_type="Credential",
        entity_id=credential.id,
        actor_user=actor_user,
        actor_organization=signing_key.organization,
        payload_json={
            "credential_code": credential.credential_code,
            "signature_verified": verified,
            "signer_name": credential.signer_name,
        },
        signature=signature,
    )
    credential.ledger_anchor_hash = event.current_hash
    credential.save(update_fields=["ledger_anchor_hash", "updated_at"])
    log_action(
        actor_user,
        action="credential.signed",
        object_type="Credential",
        object_id=credential.id,
        metadata={"credential_code": credential.credential_code},
    )
    return credential


def verify_credential_signature(credential) -> bool:
    signature_record = credential.signature_records.select_related("signing_key").first()
    if not signature_record:
        return False
    current_payload_hash = compute_payload_hash(credential.payload_json)
    current_pdf_hash = credential.pdf_hash
    return verify_message(
        signature_record.signing_key.public_key_pem,
        _signature_message_values(
            current_payload_hash,
            current_pdf_hash,
            credential.credential_code,
        ),
        signature_record.signature_value,
    )


@transaction.atomic
def publish_credential(credential, actor_user):
    if credential.current_status != CredentialStatus.SIGNED:
        raise ValueError("Khong the publish khi chung chi chua duoc ky.")
    credential.current_status = CredentialStatus.PUBLISHED
    credential.published_at = timezone.now()
    credential.save(update_fields=["current_status", "published_at", "updated_at"])
    if credential.issuance_request:
        credential.issuance_request.status = IssuanceRequestStatus.PUBLISHED
        credential.issuance_request.save(update_fields=["status", "updated_at"])

    event = commit_ledger_event(
        event_type=LedgerEventType.CREDENTIAL_PUBLISHED,
        entity_type="Credential",
        entity_id=credential.id,
        actor_user=actor_user,
        actor_organization=credential.issuer_organization,
        payload_json={"credential_code": credential.credential_code},
    )
    credential.ledger_anchor_hash = event.current_hash
    credential.save(update_fields=["ledger_anchor_hash", "updated_at"])
    log_action(
        actor_user,
        action="credential.published",
        object_type="Credential",
        object_id=credential.id,
        metadata={"credential_code": credential.credential_code},
    )
    send_credential_notification(credential, "published")
    return credential


@transaction.atomic
def revoke_credential(credential, actor_user, reason: str, decision_number: str, public_note: str = ""):
    if actor_user.role not in {
        UserRole.SYSTEM_ADMIN,
        UserRole.UNIVERSITY_ADMIN,
        UserRole.REGISTRAR,
        UserRole.AUDITOR,
    }:
        raise PermissionError("Nguoi dung khong co quyen thu hoi chung chi.")
    revocation = RevocationRecord.objects.create(
        credential=credential,
        reason=reason,
        decision_number=decision_number,
        ordered_by=actor_user,
        public_note=public_note,
    )
    credential.current_status = CredentialStatus.REVOKED
    credential.revoked_at = timezone.now()
    credential.save(update_fields=["current_status", "revoked_at", "updated_at"])
    if credential.issuance_request:
        credential.issuance_request.status = IssuanceRequestStatus.REVOKED
        credential.issuance_request.save(update_fields=["status", "updated_at"])

    event = commit_ledger_event(
        event_type=LedgerEventType.CREDENTIAL_REVOKED,
        entity_type="Credential",
        entity_id=credential.id,
        actor_user=actor_user,
        actor_organization=credential.issuer_organization,
        payload_json={
            "credential_code": credential.credential_code,
            "decision_number": decision_number,
            "reason": reason,
            "public_note": public_note,
        },
    )
    credential.ledger_anchor_hash = event.current_hash
    credential.save(update_fields=["ledger_anchor_hash", "updated_at"])
    log_action(
        actor_user,
        action="credential.revoked",
        object_type="Credential",
        object_id=credential.id,
        metadata={"credential_code": credential.credential_code, "decision_number": decision_number},
    )
    send_credential_notification(credential, "revoked")
    return revocation


@transaction.atomic
def supersede_credential(credential, actor_user, corrected_payload_updates=None, notes: str = ""):
    corrected_payload_updates = corrected_payload_updates or {}
    new_payload = _deep_merge(credential.payload_json, corrected_payload_updates)
    new_credential = Credential.objects.create(
        credential_code=generate_random_code("CRD", 8),
        serial_number=generate_random_code("SER", 8),
        verification_code=generate_random_code("VER", 8),
        public_slug=slugify(f"{credential.student.student_code}-{generate_random_code('PUB', 6)}"),
        student=credential.student,
        credential_type=credential.credential_type,
        template=credential.template,
        issuer_organization=credential.issuer_organization,
        current_status=CredentialStatus.ISSUED,
        issued_at=timezone.now(),
        payload_json=new_payload,
        payload_hash=compute_payload_hash(new_payload),
        notes=notes,
    )
    generate_qr_code(new_credential)
    render_credential_pdf(new_credential)
    new_credential.pdf_hash = compute_pdf_hash(new_credential.pdf_file.path)
    new_credential.save()

    CredentialVersion.objects.create(
        credential=new_credential,
        version_no=1,
        payload_json=new_credential.payload_json,
        payload_hash=new_credential.payload_hash,
        pdf_file=new_credential.pdf_file,
        pdf_hash=new_credential.pdf_hash,
    )

    credential.current_status = CredentialStatus.SUPERSEDED
    credential.superseded_by = new_credential
    credential.save(update_fields=["current_status", "superseded_by", "updated_at"])

    active_key = SigningKey.objects.filter(
        organization=credential.issuer_organization,
        active=True,
    ).first()
    if active_key:
        sign_credential(new_credential, active_key, actor_user, signer_title=actor_user.job_title)
        publish_credential(new_credential, actor_user)

    event = commit_ledger_event(
        event_type=LedgerEventType.CREDENTIAL_SUPERSEDED,
        entity_type="Credential",
        entity_id=credential.id,
        actor_user=actor_user,
        actor_organization=credential.issuer_organization,
        payload_json={
            "old_credential_code": credential.credential_code,
            "new_credential_code": new_credential.credential_code,
            "corrected_fields": list(corrected_payload_updates.keys()),
        },
    )
    credential.ledger_anchor_hash = event.current_hash
    credential.save(update_fields=["ledger_anchor_hash", "updated_at"])
    log_action(
        actor_user,
        action="credential.superseded",
        object_type="Credential",
        object_id=credential.id,
        metadata={
            "old_credential_code": credential.credential_code,
            "new_credential_code": new_credential.credential_code,
        },
    )
    return new_credential


@transaction.atomic
def batch_issue_credentials(requests, actor_user, signing_key=None):
    batch_no = generate_random_code("BATCH", 6)
    credentials = []
    for request_obj in requests:
        credential = issue_credential_from_request(request_obj, actor_user)
        if signing_key:
            sign_credential(credential, signing_key, actor_user, signer_title=actor_user.job_title)
            publish_credential(credential, actor_user)
        credentials.append(credential)
    return {"batch_no": batch_no, "credentials": credentials}
