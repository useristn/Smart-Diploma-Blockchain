from django.urls import path

from issuance.views import (
    ApprovalStepActionView,
    BatchIssuanceCreateView,
    BatchIssuanceDetailView,
    BatchIssuanceListView,
    CommitBatchView,
    EvaluateEligibilityView,
    IssueCredentialView,
    IssuanceRequestCreateView,
    IssuanceRequestDetailView,
    IssuanceRequestListView,
)


app_name = "issuance"

urlpatterns = [
    path("", IssuanceRequestListView.as_view(), name="list"),
    path("tao/", IssuanceRequestCreateView.as_view(), name="create"),
    path("<uuid:pk>/", IssuanceRequestDetailView.as_view(), name="detail"),
    path("<uuid:pk>/danh-gia/", EvaluateEligibilityView.as_view(), name="evaluate"),
    path("<uuid:pk>/cap-phat/", IssueCredentialView.as_view(), name="issue"),
    path(
        "<uuid:pk>/phe-duyet/<str:step_type>/<str:action>/",
        ApprovalStepActionView.as_view(),
        name="approval_action",
    ),
    # Merkle batch issuance
    path("batch/", BatchIssuanceListView.as_view(), name="batch_list"),
    path("batch/tao/", BatchIssuanceCreateView.as_view(), name="batch_create"),
    path("batch/<uuid:pk>/", BatchIssuanceDetailView.as_view(), name="batch_detail"),
    path("batch/<uuid:pk>/commit/", CommitBatchView.as_view(), name="batch_commit"),
]
