from django.db import transaction

from audit.services import log_action
from core.choices import IssuanceRequestStatus, LedgerEventType
from ledger.services import commit_ledger_event
from policy_engine.models import PolicyEvaluation, PolicyRule


def _resolve_operand(context, operand):
    if "value" in operand:
        return operand["value"]
    source = operand.get("source")
    field = operand.get("field")
    value_from = operand.get("value_from")
    base = context.get(source)
    value = getattr(base, field) if base is not None else None
    if value_from:
        from_source, from_field = value_from.split(".", 1)
        nested = context.get(from_source)
        return getattr(nested, from_field)
    return value


def _evaluate_condition(context, condition):
    left = _resolve_operand(
        context,
        {"source": condition["source"], "field": condition["field"]},
    )
    if "value" in condition:
        right = _resolve_operand(context, {"value": condition["value"]})
    else:
        right = _resolve_operand(context, {"value_from": condition["value_from"]})
    op = condition["op"]

    if op == "eq":
        return left == right
    if op == "gte":
        return left >= right
    if op == "lte":
        return left <= right
    if op == "gt":
        return left > right
    if op == "lt":
        return left < right
    if op == "in":
        return left in right
    raise ValueError(f"Unsupported policy operator: {op}")


def evaluate_rule(rule: PolicyRule, request_obj):
    context = {
        "student": request_obj.student,
        "program": request_obj.student.academic_program,
        "request": request_obj,
    }
    conditions = rule.expression_json.get("conditions", [])
    operator = rule.expression_json.get("operator", "AND").upper()

    evaluated = []
    for condition in conditions:
        result = _evaluate_condition(context, condition)
        evaluated.append({"condition": condition, "result": result})

    if not evaluated:
        final_result = True
    elif operator == "OR":
        final_result = any(item["result"] for item in evaluated)
    else:
        final_result = all(item["result"] for item in evaluated)
    return final_result, {"operator": operator, "conditions": evaluated}


@transaction.atomic
def evaluate_eligibility_rules(request_obj, actor_user=None):
    rules = PolicyRule.objects.filter(active=True).order_by("priority", "code")
    PolicyEvaluation.objects.filter(request=request_obj).delete()

    results = []
    all_passed = True
    for rule in rules:
        result, detail = evaluate_rule(rule, request_obj)
        PolicyEvaluation.objects.create(
            request=request_obj,
            rule=rule,
            result=result,
            detail_json=detail,
        )
        results.append(
            {
                "code": rule.code,
                "name": rule.name,
                "result": result,
                "detail": detail,
            }
        )
        all_passed = all_passed and result

    request_obj.evaluation_summary_json = {
        "all_passed": all_passed,
        "results": results,
    }
    if all_passed:
        request_obj.status = IssuanceRequestStatus.ACADEMIC_ELIGIBLE
        event_type = LedgerEventType.ELIGIBILITY_CHECK_PASSED
        action = "eligibility.check.passed"
    else:
        request_obj.status = IssuanceRequestStatus.UNDER_REVIEW
        event_type = LedgerEventType.ELIGIBILITY_CHECK_FAILED
        action = "eligibility.check.failed"
    request_obj.save(update_fields=["evaluation_summary_json", "status", "updated_at"])

    commit_ledger_event(
        event_type=event_type,
        entity_type="IssuanceRequest",
        entity_id=request_obj.id,
        actor_user=actor_user,
        actor_organization=getattr(actor_user, "primary_organization", None),
        payload_json=request_obj.evaluation_summary_json,
    )
    log_action(
        actor_user,
        action=action,
        object_type="IssuanceRequest",
        object_id=request_obj.id,
        metadata=request_obj.evaluation_summary_json,
    )
    return request_obj.evaluation_summary_json
