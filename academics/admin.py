from django.contrib import admin

from academics.models import AcademicProgram, Course


@admin.register(AcademicProgram)
class AcademicProgramAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "degree_type", "faculty", "total_required_credits", "min_gpa", "active")
    list_filter = ("degree_type", "active")
    search_fields = ("code", "name")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "program", "credits", "active")
    list_filter = ("active", "program")
    search_fields = ("code", "name")

# Register your models here.
