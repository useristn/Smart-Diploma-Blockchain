from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import permissions, viewsets

from ledger.models import LedgerEvent
from ledger.serializers import LedgerEventSerializer
from ledger.services import verify_ledger_chain


class LedgerEventListView(LoginRequiredMixin, ListView):
    model = LedgerEvent
    template_name = "ledger/list.html"
    context_object_name = "events"
    paginate_by = 30


class LedgerEventDetailView(LoginRequiredMixin, DetailView):
    model = LedgerEvent
    template_name = "ledger/detail.html"
    context_object_name = "event"


class LedgerVerifyView(LoginRequiredMixin, TemplateView):
    template_name = "ledger/verify.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report"] = verify_ledger_chain()
        return context


class LedgerEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LedgerEvent.objects.select_related("actor_user", "actor_organization").all()
    serializer_class = LedgerEventSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
