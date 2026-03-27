from audit.models import AuditLog


def log_action(user, action: str, object_type: str, object_id: str, metadata=None):
    return AuditLog.objects.create(
        user=user,
        action=action,
        object_type=object_type,
        object_id=str(object_id),
        metadata_json=metadata or {},
    )
