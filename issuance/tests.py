from django.core.management import call_command
from django.test import TestCase

from core.choices import ApprovalStepType, IssuanceRequestStatus
from credentials.models import CredentialTemplate, CredentialType
from issuance.services import create_issuance_request, run_approval_step
from policy_engine.services import evaluate_eligibility_rules
from students.models import Student
from accounts.models import User


class IssuanceWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data")
        cls.faculty = User.objects.get(username="faculty")
        cls.admin = User.objects.get(username="admin")
        cls.auditor = User.objects.get(username="auditor")
        cls.registrar = User.objects.get(username="registrar")
        cls.degree_type = CredentialType.objects.get(code="DEGREE")
        cls.degree_template = CredentialTemplate.objects.get(code="TPL-DEGREE-V1")

    def test_create_issuance_request(self):
        student = Student.objects.get(student_code="2101210004")
        request_obj = create_issuance_request(
            student=student,
            credential_type=self.degree_type,
            template=self.degree_template,
            requested_by=self.faculty,
            notes="create request test",
        )
        self.assertTrue(request_obj.request_code.startswith("REQ-"))
        self.assertEqual(request_obj.approval_steps.count(), 5)

    def test_rule_evaluation_pass(self):
        student = Student.objects.get(student_code="2001210001")
        request_obj = create_issuance_request(
            student=student,
            credential_type=self.degree_type,
            template=self.degree_template,
            requested_by=self.faculty,
        )
        summary = evaluate_eligibility_rules(request_obj, actor_user=self.faculty)
        self.assertTrue(summary["all_passed"])
        request_obj.refresh_from_db()
        self.assertEqual(request_obj.status, IssuanceRequestStatus.ACADEMIC_ELIGIBLE)

    def test_rule_evaluation_fail(self):
        student = Student.objects.get(student_code="2101210005")
        request_obj = create_issuance_request(
            student=student,
            credential_type=self.degree_type,
            template=self.degree_template,
            requested_by=self.faculty,
        )
        summary = evaluate_eligibility_rules(request_obj, actor_user=self.faculty)
        self.assertFalse(summary["all_passed"])

    def test_approval_workflow_reaches_final_approved(self):
        student = Student.objects.get(student_code="2001210001")
        request_obj = create_issuance_request(
            student=student,
            credential_type=self.degree_type,
            template=self.degree_template,
            requested_by=self.faculty,
        )
        evaluate_eligibility_rules(request_obj, actor_user=self.faculty)
        run_approval_step(request_obj, ApprovalStepType.ACADEMIC, self.faculty, True, "faculty ok")
        run_approval_step(request_obj, ApprovalStepType.EXAMINATION, self.admin, True, "exam ok")
        run_approval_step(request_obj, ApprovalStepType.FINANCE, self.admin, True, "finance ok")
        run_approval_step(request_obj, ApprovalStepType.DISCIPLINE, self.auditor, True, "discipline ok")
        run_approval_step(request_obj, ApprovalStepType.REGISTRAR, self.registrar, True, "registrar ok")
        request_obj.refresh_from_db()
        self.assertEqual(request_obj.status, IssuanceRequestStatus.FINAL_APPROVED)

# Create your tests here.
