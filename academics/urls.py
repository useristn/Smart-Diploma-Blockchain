from django.urls import path

from academics.views import (
    AcademicProgramCreateView,
    AcademicProgramDetailView,
    AcademicProgramListView,
    AcademicProgramUpdateView,
    CourseCreateView,
    CourseListView,
)


app_name = "academics"

urlpatterns = [
    path("chuong-trinh/", AcademicProgramListView.as_view(), name="program_list"),
    path("chuong-trinh/tao/", AcademicProgramCreateView.as_view(), name="program_create"),
    path("chuong-trinh/<uuid:pk>/", AcademicProgramDetailView.as_view(), name="program_detail"),
    path("chuong-trinh/<uuid:pk>/sua/", AcademicProgramUpdateView.as_view(), name="program_update"),
    path("hoc-phan/", CourseListView.as_view(), name="course_list"),
    path("hoc-phan/tao/", CourseCreateView.as_view(), name="course_create"),
]
