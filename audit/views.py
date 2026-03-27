from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from rest_framework import permissions, viewsets

from audit.models import AuditLog
from audit.serializers import AuditLogSerializer


class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = "audit/list.html"
    context_object_name = "logs"
    paginate_by = 30

    def get_queryset(self):
        queryset = AuditLog.objects.select_related("user")
        object_type = self.request.GET.get("object_type")
        if object_type:
            queryset = queryset.filter(object_type=object_type)
        return queryset


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("user").all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
