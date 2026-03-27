from django.urls import path

from policy_engine.views import PolicyRuleDetailView, PolicyRuleListView


app_name = "policy_engine"

urlpatterns = [
    path("", PolicyRuleListView.as_view(), name="list"),
    path("<uuid:pk>/", PolicyRuleDetailView.as_view(), name="detail"),
]
