from django.contrib import admin

from students.models import Student, StudentCourseRecord


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_code", "full_name", "academic_program", "credits_completed", "gpa", "graduation_eligible")
    list_filter = ("status", "faculty", "academic_program", "graduation_eligible", "finance_hold", "discipline_hold")
    search_fields = ("student_code", "full_name", "email")


@admin.register(StudentCourseRecord)
class StudentCourseRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "grade", "passed", "term", "year")
    list_filter = ("passed", "term", "year")

# Register your models here.
