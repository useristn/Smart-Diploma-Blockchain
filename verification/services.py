from audit.services import log_action
from core.choices import LedgerEventType
from core.utils import mask_value, short_fingerprint
from credentials.services import verify_credential_signature
from ledger.services import commit_ledger_event, verify_ledger_chain
from verification.models import VerificationLog


def get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _credential_queryset():
    from credentials.models import Credential

    return Credential.objects.select_related(
        "student",
        "credential_type",
        "issuer_organization",
        "superseded_by",
    )


def resolve_credential_lookup(value: str):
    return _credential_queryset().filter(verification_code=value).first() or _credential_queryset().filter(
        credential_code=value
    ).first() or _credential_queryset().filter(public_slug=value).first()


def build_public_verification_context(credential):
    signature_valid = verify_credential_signature(credential)
    ledger_report = verify_ledger_chain()
    latest_revocation = credential.revocation_records.first()
    public_status = "VALID" if credential.current_status == "PUBLISHED" else credential.current_status
    return {
        "credential": credential,
        "status": credential.current_status,
        "public_status": public_status,
        "owner_name": credential.student.full_name,
        "owner_code": mask_value(credential.student.student_code, 2, 2),
        "issuer_name": credential.issuer_organization.name,
        "issued_at": credential.issued_at,
        "serial_number": credential.serial_number,
        "verification_code": credential.verification_code,
        "payload_fingerprint": short_fingerprint(credential.payload_hash),
        "pdf_fingerprint": short_fingerprint(credential.pdf_hash),
        "signature_valid": signature_valid,
        "ledger_valid": ledger_report["ok"],
        "ledger_report": ledger_report,
        "public_note": latest_revocation.public_note if latest_revocation else "",
        "superseded_by": credential.superseded_by,
        "allow_public_pdf": credential.credential_type.allow_public_pdf,
    }


def record_verification(request, credential, method: str, result: str):
    VerificationLog.objects.create(
        credential=credential,
        verification_method=method,
        requester_ip=get_client_ip(request),
        requester_user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
        result=result,
    )
    commit_ledger_event(
        event_type=LedgerEventType.CREDENTIAL_VERIFIED,
        entity_type="Credential",
        entity_id=credential.id,
        actor_user=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
        actor_organization=getattr(getattr(request, "user", None), "primary_organization", None),
        payload_json={"verification_method": method, "result": result},
    )
    log_action(
        request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
        action="credential.verified",
        object_type="Credential",
        object_id=credential.id,
        metadata={"verification_method": method, "result": result},
    )


def verify_lookup(request, value: str, method: str):
    credential = resolve_credential_lookup(value)
    if not credential:
        return None, None
    context = build_public_verification_context(credential)
    record_verification(request, credential, method, credential.current_status)
    return credential, context
