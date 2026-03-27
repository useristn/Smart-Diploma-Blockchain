from django.db import transaction
from django.utils import timezone

from core.utils import canonicalize_json, sha256_digest
from ledger.models import LedgerEvent


def build_event_hash(
    sequence_no: int,
    timestamp,
    event_type: str,
    entity_type: str,
    entity_id: str,
    actor_user_id,
    actor_organization_id,
    payload_json,
    previous_hash: str,
) -> str:
    raw = "|".join(
        [
            str(sequence_no),
            timestamp.isoformat(),
            event_type,
            entity_type,
            str(entity_id),
            str(actor_user_id or ""),
            str(actor_organization_id or ""),
            canonicalize_json(payload_json),
            previous_hash or "",
        ]
    )
    return sha256_digest(raw)


@transaction.atomic
def commit_ledger_event(
    *,
    event_type: str,
    entity_type: str,
    entity_id,
    actor_user=None,
    actor_organization=None,
    payload_json=None,
    signature: str = "",
    batch_no: str = "",
):
    last_event = LedgerEvent.objects.order_by("-sequence_no").first()
    sequence_no = (last_event.sequence_no if last_event else 0) + 1
    previous_hash = last_event.current_hash if last_event else ""
    placeholder_hash = sha256_digest(f"pending|{sequence_no}|{timezone.now().isoformat()}")
    event = LedgerEvent.objects.create(
        sequence_no=sequence_no,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=str(entity_id),
        actor_user=actor_user,
        actor_organization=actor_organization,
        payload_json=payload_json or {},
        previous_hash=previous_hash,
        current_hash=placeholder_hash,
        signature=signature,
        batch_no=batch_no,
    )
    event.current_hash = build_event_hash(
        sequence_no=sequence_no,
        timestamp=event.created_at,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=str(entity_id),
        actor_user_id=getattr(actor_user, "id", ""),
        actor_organization_id=getattr(actor_organization, "id", ""),
        payload_json=payload_json or {},
        previous_hash=previous_hash,
    )
    event.save(update_fields=["current_hash"])
    return event


def verify_ledger_chain(limit=None):
    queryset = list(LedgerEvent.objects.order_by("sequence_no"))
    if limit:
        queryset = queryset[-limit:]

    previous_hash = ""
    issues = []
    checked = 0
    for event in queryset:
        checked += 1
        expected_hash = build_event_hash(
            sequence_no=event.sequence_no,
            timestamp=event.created_at,
            event_type=event.event_type,
            entity_type=event.entity_type,
            entity_id=event.entity_id,
            actor_user_id=event.actor_user_id,
            actor_organization_id=event.actor_organization_id,
            payload_json=event.payload_json,
            previous_hash=event.previous_hash,
        )
        if event.previous_hash != previous_hash:
            issues.append(
                {
                    "sequence_no": event.sequence_no,
                    "issue": "previous_hash_mismatch",
                    "expected_previous_hash": previous_hash,
                    "stored_previous_hash": event.previous_hash,
                }
            )
        if event.current_hash != expected_hash:
            issues.append(
                {
                    "sequence_no": event.sequence_no,
                    "issue": "current_hash_mismatch",
                    "expected_current_hash": expected_hash,
                    "stored_current_hash": event.current_hash,
                }
            )
        previous_hash = event.current_hash

    return {
        "ok": not issues,
        "checked": checked,
        "issues": issues,
        "last_hash": previous_hash,
    }
