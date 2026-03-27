from django.conf import settings
from django.db import models

from core.choices import StudentStatus
from core.models import TimeStampedModel, UUIDPrimaryKeyModel


class Student(UUIDPrimaryKeyModel, TimeStampedModel):
    student_code = models.CharField(max_length=32, unique=True)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField()
    national_id = models.CharField(max_length=32, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="student_profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    faculty = models.ForeignKey(
        "organizations.Organization",
        related_name="students",
        on_delete=models.PROTECT,
    )
    academic_program = models.ForeignKey(
        "academics.AcademicProgram",
        related_name="students",
        on_delete=models.PROTECT,
    )
    cohort = models.CharField(max_length=32)
    status = models.CharField(
        max_length=16,
        choices=StudentStatus.choices,
        default=StudentStatus.ACTIVE,
    )
    credits_completed = models.PositiveIntegerField(default=0)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    finance_hold = models.BooleanField(default=False)
    discipline_hold = models.BooleanField(default=False)
    graduation_eligible = models.BooleanField(default=False)
    graduation_status = models.CharField(max_length=120, blank=True)
    evidence_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["student_code"]

    def __str__(self):
        return f"{self.student_code} - {self.full_name}"


class StudentCourseRecord(UUIDPrimaryKeyModel, TimeStampedModel):
    student = models.ForeignKey(
        Student,
        related_name="course_records",
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        "academics.Course",
        related_name="student_records",
        on_delete=models.CASCADE,
    )
    grade = models.CharField(max_length=4)
    passed = models.BooleanField(default=False)
    term = models.CharField(max_length=16)
    year = models.PositiveIntegerField()

    class Meta:
        ordering = ["-year", "term", "course__code"]
        unique_together = ("student", "course", "term", "year")

# Create your models here.
