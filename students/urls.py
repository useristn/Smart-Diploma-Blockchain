from django.urls import path

from students.views import StudentCreateView, StudentDetailView, StudentListView, StudentPortalView, StudentUpdateView


app_name = "students"

urlpatterns = [
    path("", StudentListView.as_view(), name="list"),
    path("portal/", StudentPortalView.as_view(), name="portal"),
    path("tao/", StudentCreateView.as_view(), name="create"),
    path("<uuid:pk>/", StudentDetailView.as_view(), name="detail"),
    path("<uuid:pk>/sua/", StudentUpdateView.as_view(), name="update"),
]
