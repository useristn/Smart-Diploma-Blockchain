from django.urls import path

from ledger.views import LedgerEventDetailView, LedgerEventListView, LedgerVerifyView


app_name = "ledger"

urlpatterns = [
    path("", LedgerEventListView.as_view(), name="list"),
    path("kiem-tra/", LedgerVerifyView.as_view(), name="verify"),
    path("<uuid:pk>/", LedgerEventDetailView.as_view(), name="detail"),
]
