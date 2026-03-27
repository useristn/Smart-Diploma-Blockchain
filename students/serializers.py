from rest_framework import serializers

from students.models import Student, StudentCourseRecord


class StudentSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source="faculty.name", read_only=True)
    academic_program_name = serializers.CharField(source="academic_program.name", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "student_code",
            "full_name",
            "date_of_birth",
            "email",
            "faculty",
            "faculty_name",
            "academic_program",
            "academic_program_name",
            "cohort",
            "status",
            "credits_completed",
            "gpa",
            "finance_hold",
            "discipline_hold",
            "graduation_eligible",
            "graduation_status",
        ]


class StudentCourseRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = StudentCourseRecord
        fields = [
            "id",
            "student",
            "student_name",
            "course",
            "course_name",
            "grade",
            "passed",
            "term",
            "year",
        ]
