from django import forms

from students.models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_code",
            "full_name",
            "date_of_birth",
            "email",
            "national_id",
            "user",
            "faculty",
            "academic_program",
            "cohort",
            "status",
            "credits_completed",
            "gpa",
            "finance_hold",
            "discipline_hold",
            "graduation_eligible",
            "graduation_status",
            "evidence_json",
        ]
