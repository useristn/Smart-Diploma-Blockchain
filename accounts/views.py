from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework import permissions, viewsets

from accounts.forms import MembershipForm, ProfileForm, UserForm
from accounts.models import OrganizationMembership, User
from accounts.permissions import RoleRequiredMixin
from accounts.serializers import MembershipSerializer, UserSerializer
from core.choices import UserRole


class AppLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class AppLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class AppPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("accounts:profile")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Đã cập nhật hồ sơ.")
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN)
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"


class UserCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN)
    model = User
    form_class = UserForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        messages.success(self.request, "Đã tạo tài khoản mới.")
        return super().form_valid(form)


class MembershipListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN)
    model = OrganizationMembership
    template_name = "accounts/membership_list.html"
    context_object_name = "memberships"


class MembershipCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN)
    model = OrganizationMembership
    form_class = MembershipForm
    template_name = "accounts/membership_form.html"
    success_url = reverse_lazy("accounts:membership_list")

    def form_valid(self, form):
        messages.success(self.request, "Đã gán membership.")
        return super().form_valid(form)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("primary_organization").all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = OrganizationMembership.objects.select_related("user", "organization").all()
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
