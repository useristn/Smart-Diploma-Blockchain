from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from rest_framework import permissions, viewsets

from policy_engine.models import PolicyEvaluation, PolicyRule
from policy_engine.serializers import PolicyEvaluationSerializer, PolicyRuleSerializer


class PolicyRuleListView(LoginRequiredMixin, ListView):
    model = PolicyRule
    template_name = "issuance/policy_rule_list.html"
    context_object_name = "rules"


class PolicyRuleDetailView(LoginRequiredMixin, DetailView):
    model = PolicyRule
    template_name = "issuance/policy_rule_detail.html"
    context_object_name = "rule"


class PolicyRuleViewSet(viewsets.ModelViewSet):
    queryset = PolicyRule.objects.all()
    serializer_class = PolicyRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class PolicyEvaluationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PolicyEvaluation.objects.select_related("rule", "request").all()
    serializer_class = PolicyEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
