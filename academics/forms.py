from django import forms

from academics.models import AcademicProgram, Course


class AcademicProgramForm(forms.ModelForm):
    class Meta:
        model = AcademicProgram
        fields = [
            "code",
            "name",
            "description",
            "degree_type",
            "total_required_credits",
            "min_gpa",
            "faculty",
            "policy_config_json",
            "active",
        ]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "code",
            "name",
            "description",
            "credits",
            "program",
            "active",
        ]
