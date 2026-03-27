from django.contrib import admin

from accounts.models import OrganizationMembership, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "email", "role", "primary_organization", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("username", "full_name", "email")


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "role", "is_primary", "is_active")
    list_filter = ("role", "is_primary", "is_active")

# Register your models here.
