from rest_framework import serializers

from policy_engine.models import PolicyEvaluation, PolicyRule


class PolicyRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyRule
        fields = [
            "id",
            "code",
            "name",
            "description",
            "rule_type",
            "expression_json",
            "priority",
            "active",
        ]


class PolicyEvaluationSerializer(serializers.ModelSerializer):
    rule_name = serializers.CharField(source="rule.name", read_only=True)

    class Meta:
        model = PolicyEvaluation
        fields = [
            "id",
            "request",
            "rule",
            "rule_name",
            "result",
            "detail_json",
            "executed_at",
        ]
