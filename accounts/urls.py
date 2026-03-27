from django.urls import path

from accounts.views import (
    AppLoginView,
    AppLogoutView,
    AppPasswordChangeView,
    MembershipCreateView,
    MembershipListView,
    ProfileUpdateView,
    UserCreateView,
    UserListView,
)


app_name = "accounts"

urlpatterns = [
    path("dang-nhap/", AppLoginView.as_view(), name="login"),
    path("dang-xuat/", AppLogoutView.as_view(), name="logout"),
    path("ho-so/", ProfileUpdateView.as_view(), name="profile"),
    path("doi-mat-khau/", AppPasswordChangeView.as_view(), name="change_password"),
    path("nguoi-dung/", UserListView.as_view(), name="user_list"),
    path("nguoi-dung/tao/", UserCreateView.as_view(), name="user_create"),
    path("membership/", MembershipListView.as_view(), name="membership_list"),
    path("membership/tao/", MembershipCreateView.as_view(), name="membership_create"),
]
