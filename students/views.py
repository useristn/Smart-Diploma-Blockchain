from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView
from rest_framework import permissions, viewsets

from accounts.permissions import RoleRequiredMixin
from core.choices import UserRole
from students.forms import StudentForm
from students.models import Student, StudentCourseRecord
from students.serializers import StudentCourseRecordSerializer, StudentSerializer


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/list.html"
    context_object_name = "students"


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course_records"] = self.object.course_records.select_related("course")
        context["credentials"] = self.object.credentials.select_related("credential_type")
        return context


class StudentCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN, UserRole.FACULTY_ADMIN)
    model = Student
    form_class = StudentForm
    template_name = "students/form.html"
    success_url = reverse_lazy("students:list")

    def form_valid(self, form):
        messages.success(self.request, "Đã tạo sinh viên.")
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN, UserRole.FACULTY_ADMIN)
    model = Student
    form_class = StudentForm
    template_name = "students/form.html"
    success_url = reverse_lazy("students:list")


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Student.objects.select_related("faculty", "academic_program")
        user = self.request.user
        if user.role == UserRole.STUDENT:
            return qs.filter(user=user)
        return qs.all()


class StudentCourseRecordViewSet(viewsets.ModelViewSet):
    serializer_class = StudentCourseRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = StudentCourseRecord.objects.select_related("student", "course")
        user = self.request.user
        if user.role == UserRole.STUDENT:
            return qs.filter(student__user=user)
        return qs.all()
    permission_classes = [permissions.IsAuthenticated]


class StudentPortalView(LoginRequiredMixin, TemplateView):
    """Self-service portal for authenticated students."""

    template_name = "students/portal.html"

    def dispatch(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        if request.user.is_authenticated and request.user.role != UserRole.STUDENT:
            return redirect("core:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = self.request.user.student_profile
        except Exception:
            student = None
        context["student"] = student
        if student:
            context["credentials"] = student.credentials.select_related(
                "credential_type", "issuer_organization"
            ).order_by("-issued_at", "-created_at")
            context["issuance_requests"] = student.issuance_requests.select_related(
                "credential_type"
            ).order_by("-requested_at")
        return context
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
