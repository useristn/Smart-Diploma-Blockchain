from django.db import models

from core.models import NamedModel


class AcademicProgram(NamedModel):
    degree_type = models.CharField(max_length=120)
    total_required_credits = models.PositiveIntegerField(default=120)
    min_gpa = models.DecimalField(max_digits=4, decimal_places=2, default=2.00)
    faculty = models.ForeignKey(
        "organizations.Organization",
        related_name="academic_programs",
        on_delete=models.PROTECT,
    )
    policy_config_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["code"]


class Course(NamedModel):
    credits = models.PositiveIntegerField(default=3)
    program = models.ForeignKey(
        AcademicProgram,
        related_name="courses",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["program__code", "code"]

# Create your models here.
