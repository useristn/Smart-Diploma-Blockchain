from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework import permissions, viewsets

from accounts.permissions import RoleRequiredMixin
from core.choices import UserRole
from organizations.forms import OrganizationForm
from organizations.models import Organization
from organizations.serializers import OrganizationSerializer


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = "organizations/list.html"
    context_object_name = "organizations"


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = "organizations/detail.html"
    context_object_name = "organization"


class OrganizationCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN)
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/form.html"
    success_url = reverse_lazy("organizations:list")

    def form_valid(self, form):
        messages.success(self.request, "Đã tạo tổ chức.")
        return super().form_valid(form)


class OrganizationUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN)
    model = Organization
    form_class = OrganizationForm
    template_name = "organizations/form.html"
    success_url = reverse_lazy("organizations:list")

    def form_valid(self, form):
        messages.success(self.request, "Đã cập nhật tổ chức.")
        return super().form_valid(form)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.select_related("parent").all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
