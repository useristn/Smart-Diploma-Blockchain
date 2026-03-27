from django.contrib import admin

from organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "organization_type", "parent", "can_write_ledger", "can_approve", "active")
    list_filter = ("organization_type", "can_write_ledger", "can_approve", "active")
    search_fields = ("code", "name")

# Register your models here.
