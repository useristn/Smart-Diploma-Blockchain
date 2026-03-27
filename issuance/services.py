from django.db import transaction
from django.utils import timezone

from audit.services import log_action
from core.choices import (
    ApprovalStatus,
    ApprovalStepType,
    IssuanceRequestStatus,
    LedgerEventType,
    UserRole,
)
from core.notifications import send_approval_notification
from core.utils import compute_merkle_proof, compute_merkle_root, generate_random_code
from issuance.models import ApprovalStep, BatchIssuance, IssuanceRequest
from ledger.services import commit_ledger_event


DEFAULT_APPROVAL_FLOW = [
    (ApprovalStepType.ACADEMIC, UserRole.FACULTY_ADMIN),
    (ApprovalStepType.EXAMINATION, UserRole.EXAMINATION_OFFICER),
    (ApprovalStepType.FINANCE, UserRole.UNIVERSITY_ADMIN),
    (ApprovalStepType.DISCIPLINE, UserRole.AUDITOR),
    (ApprovalStepType.REGISTRAR, UserRole.REGISTRAR),
]

STATUS_AFTER_STEP = {
    ApprovalStepType.ACADEMIC: IssuanceRequestStatus.ACADEMIC_ELIGIBLE,
    ApprovalStepType.FINANCE: IssuanceRequestStatus.FINANCE_CLEARED,
    ApprovalStepType.DISCIPLINE: IssuanceRequestStatus.DISCIPLINE_CLEARED,
    ApprovalStepType.REGISTRAR: IssuanceRequestStatus.FINAL_APPROVED,
}


@transaction.atomic
def create_issuance_request(student, credential_type, template, requested_by, notes=""):
    request_obj = IssuanceRequest.objects.create(
        request_code=generate_random_code("REQ", 8),
        student=student,
        credential_type=credential_type,
        template=template,
        requested_by=requested_by,
        status=IssuanceRequestStatus.SUBMITTED,
        notes=notes,
    )
    for step_type, assigned_role in DEFAULT_APPROVAL_FLOW:
        ApprovalStep.objects.create(
            request=request_obj,
            step_type=step_type,
            assigned_to_role=assigned_role,
        )

    commit_ledger_event(
        event_type=LedgerEventType.ISSUANCE_REQUEST_CREATED,
        entity_type="IssuanceRequest",
        entity_id=request_obj.id,
        actor_user=requested_by,
        actor_organization=getattr(requested_by, "primary_organization", None),
        payload_json={
            "request_code": request_obj.request_code,
            "student_code": student.student_code,
            "credential_type": credential_type.code,
        },
    )
    log_action(
        requested_by,
        action="issuance_request.created",
        object_type="IssuanceRequest",
        object_id=request_obj.id,
        metadata={"request_code": request_obj.request_code},
    )
    return request_obj


def is_final_approved(request_obj) -> bool:
    return request_obj.status == IssuanceRequestStatus.FINAL_APPROVED and not request_obj.approval_steps.exclude(
        status=ApprovalStatus.APPROVED
    ).exists()


@transaction.atomic
def run_approval_step(request_obj, step_type: str, actor_user, approved: bool, note: str = ""):
    if request_obj.status in {
        IssuanceRequestStatus.REJECTED,
        IssuanceRequestStatus.PUBLISHED,
        IssuanceRequestStatus.REVOKED,
    }:
        raise ValueError("Ho so khong con cho phe duyet.")

    step = request_obj.approval_steps.get(step_type=step_type)
    if step.status != ApprovalStatus.PENDING:
        raise ValueError("Buoc phe duyet nay da duoc xu ly.")
    if actor_user.role not in {step.assigned_to_role, UserRole.SYSTEM_ADMIN}:
        raise PermissionError("Nguoi dung khong co quyen duyet buoc nay.")

    step.status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
    step.approved_by = actor_user
    step.approved_at = timezone.now()
    step.note = note
    step.save(update_fields=["status", "approved_by", "approved_at", "note", "updated_at"])

    if approved:
        request_obj.status = STATUS_AFTER_STEP.get(step_type, request_obj.status)
        event_type = LedgerEventType.APPROVAL_GRANTED
    else:
        request_obj.status = IssuanceRequestStatus.REJECTED
        event_type = LedgerEventType.APPROVAL_REJECTED
    request_obj.save(update_fields=["status", "updated_at"])

    payload = {
        "request_code": request_obj.request_code,
        "step_type": step_type,
        "approved": approved,
        "approved_by": actor_user.username,
        "note": note,
        "current_status": request_obj.status,
    }
    commit_ledger_event(
        event_type=event_type,
        entity_type="IssuanceRequest",
        entity_id=request_obj.id,
        actor_user=actor_user,
        actor_organization=getattr(actor_user, "primary_organization", None),
        payload_json=payload,
    )
    log_action(
        actor_user,
        action="approval.step.run",
        object_type="IssuanceRequest",
        object_id=request_obj.id,
        metadata=payload,
    )
    send_approval_notification(request_obj, step, approved)
    return step


@transaction.atomic
def create_batch_issuance(*, name: str, description: str, request_ids: list, actor_user):
    """Create a BatchIssuance record with the given IssuanceRequests."""
    batch = BatchIssuance.objects.create(
        batch_code=generate_random_code("BATCH", 8),
        name=name,
        description=description,
    )
    batch.requests.set(IssuanceRequest.objects.filter(id__in=request_ids))
    log_action(
        actor_user,
        action="batch.created",
        object_type="BatchIssuance",
        object_id=batch.id,
        metadata={"batch_code": batch.batch_code, "request_count": len(request_ids)},
    )
    return batch


@transaction.atomic
def commit_batch_issuance(batch: BatchIssuance, actor_user):
    """Compute Merkle root over credential payload hashes and anchor to ledger.

    Only credentials that have a payload_hash (i.e. have been issued) are
    included.  The batch is idempotent – re-committing raises ValueError.
    """
    from credentials.models import Credential
    from ledger.models import LedgerEvent

    if batch.is_committed:
        raise ValueError("Batch đã được commit vào ledger.")

    credentials = list(
        Credential.objects.filter(
            issuance_request__in=batch.requests.all()
        ).exclude(payload_hash="")
    )
    if not credentials:
        raise ValueError("Batch chưa có credential nào có payload hash. Hãy issue các chứng chỉ trước.")

    hashes = sorted([c.payload_hash for c in credentials])
    merkle_root = compute_merkle_root(hashes)

    batch.merkle_root = merkle_root
    batch.committed_at = timezone.now()
    batch.committed_by = actor_user
    batch.save(update_fields=["merkle_root", "committed_at", "committed_by", "updated_at"])

    event = commit_ledger_event(
        event_type=LedgerEventType.BATCH_COMMITTED,
        entity_type="BatchIssuance",
        entity_id=batch.id,
        actor_user=actor_user,
        actor_organization=getattr(actor_user, "primary_organization", None),
        payload_json={
            "batch_code": batch.batch_code,
            "merkle_root": merkle_root,
            "credential_count": len(hashes),
            "leaf_hashes": hashes,
        },
        batch_no=batch.batch_code,
    )

    # Back-annotate all related ledger credential events with block/batch info
    LedgerEvent.objects.filter(
        entity_type="Credential",
        entity_id__in=[str(c.id) for c in credentials],
    ).update(block_no=event.sequence_no, batch_no=batch.batch_code)

    log_action(
        actor_user,
        action="batch.committed",
        object_type="BatchIssuance",
        object_id=batch.id,
        metadata={
            "batch_code": batch.batch_code,
            "merkle_root": merkle_root,
            "credential_count": len(hashes),
        },
    )
    return batch, merkle_root


def get_merkle_proof_for_credential(batch: BatchIssuance, credential_id: str) -> dict:
    """Return Merkle proof for a single credential in a committed batch."""
    from credentials.models import Credential

    if not batch.is_committed:
        return {"error": "Batch chưa được commit."}

    credentials = list(
        Credential.objects.filter(
            issuance_request__in=batch.requests.all()
        ).exclude(payload_hash="")
    )
    hashes = sorted([c.payload_hash for c in credentials])
    cred = next((c for c in credentials if str(c.id) == credential_id), None)
    if not cred:
        return {"error": "Credential không thuộc batch này."}

    proof = compute_merkle_proof(hashes, cred.payload_hash)
    return {
        "credential_code": cred.credential_code,
        "leaf_hash": cred.payload_hash,
        "merkle_root": batch.merkle_root,
        "proof": proof,
    }
