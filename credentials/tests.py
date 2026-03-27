from django.core.management import call_command
from django.test import TestCase

from core.choices import ApprovalStepType
from credentials.models import Credential, CredentialTemplate, CredentialType, SigningKey
from credentials.services import (
    compute_pdf_hash,
    issue_credential_from_request,
    publish_credential,
    sign_credential,
    supersede_credential,
    verify_credential_signature,
)
from issuance.services import create_issuance_request, run_approval_step
from policy_engine.services import evaluate_eligibility_rules
from students.models import Student
from accounts.models import User


class CredentialServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data")
        cls.faculty = User.objects.get(username="faculty")
        cls.admin = User.objects.get(username="admin")
        cls.auditor = User.objects.get(username="auditor")
        cls.registrar = User.objects.get(username="registrar")
        cls.signer = User.objects.get(username="signer")
        cls.degree_type = CredentialType.objects.get(code="DEGREE")
        cls.degree_template = CredentialTemplate.objects.get(code="TPL-DEGREE-V1")
        cls.signing_key = SigningKey.objects.get(key_name="Demo Registrar Key")

    def _final_approved_request(self, student_code="SV001"):
        student = Student.objects.get(student_code=student_code)
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
        return request_obj

    def test_cannot_publish_without_sign(self):
        request_obj = self._final_approved_request()
        credential = issue_credential_from_request(request_obj, self.registrar)
        with self.assertRaises(ValueError):
            publish_credential(credential, self.registrar)

    def test_sign_credential_success(self):
        request_obj = self._final_approved_request()
        credential = issue_credential_from_request(request_obj, self.registrar)
        sign_credential(credential, self.signing_key, self.signer, signer_title="Signer")
        credential.refresh_from_db()
        self.assertEqual(credential.current_status, "SIGNED")

    def test_verify_signature_success(self):
        request_obj = self._final_approved_request()
        credential = issue_credential_from_request(request_obj, self.registrar)
        sign_credential(credential, self.signing_key, self.signer, signer_title="Signer")
        self.assertTrue(verify_credential_signature(credential))

    def test_verify_signature_fail_when_payload_tampered(self):
        request_obj = self._final_approved_request()
        credential = issue_credential_from_request(request_obj, self.registrar)
        sign_credential(credential, self.signing_key, self.signer, signer_title="Signer")
        credential.payload_json["student"]["full_name"] = "Tampered Name"
        self.assertFalse(verify_credential_signature(credential))

    def test_pdf_hash_verify(self):
        credential = Credential.objects.filter(current_status="PUBLISHED").first()
        self.assertEqual(compute_pdf_hash(credential.pdf_file.path), credential.pdf_hash)

    def test_superseded_credential_points_to_new_version(self):
        source = Credential.objects.filter(current_status="SUPERSEDED").first()
        self.assertIsNotNone(source.superseded_by)

    def test_supersede_service_creates_new_credential(self):
        request_obj = self._final_approved_request("SV002")
        credential = issue_credential_from_request(request_obj, self.registrar)
        sign_credential(credential, self.signing_key, self.signer, signer_title="Signer")
        publish_credential(credential, self.registrar)
        replacement = supersede_credential(
            credential,
            actor_user=self.registrar,
            corrected_payload_updates={"student": {"full_name": "Replacement Name"}},
            notes="fix typo",
        )
        credential.refresh_from_db()
        self.assertEqual(credential.current_status, "SUPERSEDED")
        self.assertEqual(replacement.payload_json["student"]["full_name"], "Replacement Name")

# Create your tests here.
