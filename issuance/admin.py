from django.contrib import admin

from issuance.models import ApprovalStep, IssuanceRequest


@admin.register(IssuanceRequest)
class IssuanceRequestAdmin(admin.ModelAdmin):
    list_display = ("request_code", "student", "credential_type", "status", "requested_by", "requested_at")
    list_filter = ("status", "credential_type")
    search_fields = ("request_code", "student__student_code", "student__full_name")


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ("request", "step_type", "assigned_to_role", "approved_by", "status", "approved_at")
    list_filter = ("step_type", "status")

# Register your models here.
