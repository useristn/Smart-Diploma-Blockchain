from django.urls import path

from credentials.views import (
    CredentialDetailView,
    CredentialListView,
    PublishCredentialView,
    RevokeCredentialView,
    SignCredentialView,
    SupersedeCredentialView,
)


app_name = "credentials"

urlpatterns = [
    path("", CredentialListView.as_view(), name="list"),
    path("<uuid:pk>/", CredentialDetailView.as_view(), name="detail"),
    path("<uuid:pk>/ky/", SignCredentialView.as_view(), name="sign"),
    path("<uuid:pk>/publish/", PublishCredentialView.as_view(), name="publish"),
    path("<uuid:pk>/thu-hoi/", RevokeCredentialView.as_view(), name="revoke"),
    path("<uuid:pk>/thay-the/", SupersedeCredentialView.as_view(), name="supersede"),
]
