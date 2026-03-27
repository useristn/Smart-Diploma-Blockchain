from django.urls import path

from public_portal.views import PublicVerificationDetailView, PublicVerificationHomeView


app_name = "public_portal"

urlpatterns = [
    path("", PublicVerificationHomeView.as_view(), name="home"),
    path("tra-cuu/<slug:slug>/", PublicVerificationDetailView.as_view(), name="detail"),
]
