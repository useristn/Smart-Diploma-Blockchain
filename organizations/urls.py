from django.urls import path

from organizations.views import (
    OrganizationCreateView,
    OrganizationDetailView,
    OrganizationListView,
    OrganizationUpdateView,
)


app_name = "organizations"

urlpatterns = [
    path("", OrganizationListView.as_view(), name="list"),
    path("tao/", OrganizationCreateView.as_view(), name="create"),
    path("<uuid:pk>/", OrganizationDetailView.as_view(), name="detail"),
    path("<uuid:pk>/sua/", OrganizationUpdateView.as_view(), name="update"),
]
