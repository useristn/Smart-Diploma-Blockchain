from rest_framework import serializers

from academics.models import AcademicProgram, Course


class AcademicProgramSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source="faculty.name", read_only=True)

    class Meta:
        model = AcademicProgram
        fields = [
            "id",
            "code",
            "name",
            "description",
            "degree_type",
            "total_required_credits",
            "min_gpa",
            "faculty",
            "faculty_name",
            "policy_config_json",
            "active",
        ]


class CourseSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "code",
            "name",
            "description",
            "credits",
            "program",
            "program_name",
            "active",
        ]
