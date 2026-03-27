from django.contrib import admin

from ledger.models import LedgerEvent


@admin.register(LedgerEvent)
class LedgerEventAdmin(admin.ModelAdmin):
    list_display = ("sequence_no", "event_type", "entity_type", "entity_id", "actor_user", "created_at", "is_valid")
    list_filter = ("event_type", "entity_type", "is_valid")
    search_fields = ("entity_id", "current_hash")

# Register your models here.
