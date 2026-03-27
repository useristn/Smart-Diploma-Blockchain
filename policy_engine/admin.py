from django.contrib import admin

from policy_engine.models import PolicyEvaluation, PolicyRule


@admin.register(PolicyRule)
class PolicyRuleAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "rule_type", "priority", "active")
    list_filter = ("rule_type", "active")
    search_fields = ("code", "name")


@admin.register(PolicyEvaluation)
class PolicyEvaluationAdmin(admin.ModelAdmin):
    list_display = ("request", "rule", "result", "executed_at")
    list_filter = ("result", "rule")

# Register your models here.
