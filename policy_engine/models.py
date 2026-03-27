from django.db import models

from core.choices import PolicyRuleType
from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class PolicyRule(UUIDPrimaryKeyModel, TimeStampedModel):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    rule_type = models.CharField(
        max_length=24,
        choices=PolicyRuleType.choices,
        default=PolicyRuleType.ELIGIBILITY,
    )
    expression_json = models.JSONField(default=dict, blank=True)
    priority = models.PositiveIntegerField(default=100)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["priority", "code"]

    def __str__(self):
        return self.name


class PolicyEvaluation(UUIDPrimaryKeyModel, TimeStampedModel):
    request = models.ForeignKey(
        "issuance.IssuanceRequest",
        related_name="policy_evaluations",
        on_delete=models.CASCADE,
    )
    rule = models.ForeignKey(
        PolicyRule,
        related_name="evaluations",
        on_delete=models.CASCADE,
    )
    result = models.BooleanField(default=False)
    detail_json = models.JSONField(default=dict, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-executed_at", "rule__priority"]

# Create your models here.
