from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework import permissions, viewsets

from academics.forms import AcademicProgramForm, CourseForm
from academics.models import AcademicProgram, Course
from academics.serializers import AcademicProgramSerializer, CourseSerializer
from accounts.permissions import RoleRequiredMixin
from core.choices import UserRole


class AcademicProgramListView(LoginRequiredMixin, ListView):
    model = AcademicProgram
    template_name = "academics/program_list.html"
    context_object_name = "programs"


class AcademicProgramDetailView(LoginRequiredMixin, DetailView):
    model = AcademicProgram
    template_name = "academics/program_detail.html"
    context_object_name = "program"


class AcademicProgramCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN, UserRole.FACULTY_ADMIN)
    model = AcademicProgram
    form_class = AcademicProgramForm
    template_name = "academics/program_form.html"
    success_url = reverse_lazy("academics:program_list")

    def form_valid(self, form):
        messages.success(self.request, "Đã tạo chương trình.")
        return super().form_valid(form)


class AcademicProgramUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN, UserRole.FACULTY_ADMIN)
    model = AcademicProgram
    form_class = AcademicProgramForm
    template_name = "academics/program_form.html"
    success_url = reverse_lazy("academics:program_list")


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "academics/course_list.html"
    context_object_name = "courses"


class CourseCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = (UserRole.SYSTEM_ADMIN, UserRole.UNIVERSITY_ADMIN, UserRole.FACULTY_ADMIN)
    model = Course
    form_class = CourseForm
    template_name = "academics/course_form.html"
    success_url = reverse_lazy("academics:course_list")


class AcademicProgramViewSet(viewsets.ModelViewSet):
    queryset = AcademicProgram.objects.select_related("faculty").all()
    serializer_class = AcademicProgramSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("program").all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
