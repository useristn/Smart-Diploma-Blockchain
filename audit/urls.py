from django.urls import path

from audit.views import AuditLogListView


app_name = "audit"

urlpatterns = [
    path("", AuditLogListView.as_view(), name="list"),
]
