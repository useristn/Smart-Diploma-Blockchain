from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from accounts.models import OrganizationMembership, User
from academics.models import AcademicProgram, Course
from core.choices import ApprovalStepType, OrganizationType, UserRole
from core.signing import generate_rsa_key_pair
from credentials.models import Credential, CredentialTemplate, CredentialType, SigningKey
from credentials.services import (
    issue_credential_from_request,
    publish_credential,
    revoke_credential,
    sign_credential,
    supersede_credential,
)
from issuance.models import IssuanceRequest
from issuance.services import create_issuance_request, run_approval_step
from organizations.models import Organization
from policy_engine.models import PolicyRule
from policy_engine.services import evaluate_eligibility_rules
from students.models import Student, StudentCourseRecord


class Command(BaseCommand):
    help = "Seed the demo university blockchain credential system with end-to-end sample data."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Flush current data before seeding.")

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write(self.style.WARNING("Flushing existing data..."))
            call_command("flush", "--noinput")

        if Credential.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Demo credentials already exist. Use --reset to rebuild the full demo dataset."
                )
            )
            return

        organizations = self._seed_organizations()
        users = self._seed_users(organizations)
        programs = self._seed_programs(organizations)
        self._seed_courses(programs)
        students = self._seed_students(organizations, programs, users)
        credential_types, templates = self._seed_credential_types()
        self._seed_policy_rules()
        signing_key = self._ensure_signing_key(organizations["registrar"])
        self._seed_demo_flows(users, students, credential_types, templates, signing_key)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
        self.stdout.write("Demo users:")
        self.stdout.write("  admin / admin12345")
        self.stdout.write("  registrar / registrar12345")
        self.stdout.write("  faculty / faculty12345")
        self.stdout.write("  signer / signer12345")
        self.stdout.write("  auditor / auditor12345")
        self.stdout.write("  studenta / student12345")
        self.stdout.write("  studentb / student12345")

    def _seed_organizations(self):
        university, _ = Organization.objects.update_or_create(
            code="UNI",
            defaults={
                "name": "Đại học Demo Blockchain",
                "organization_type": OrganizationType.UNIVERSITY,
                "can_write_ledger": True,
                "can_approve": True,
                "is_validator": True,
                "public_visible": True,
            },
        )
        training, _ = Organization.objects.update_or_create(
            code="TRAIN",
            defaults={
                "name": "Phòng Đào Tạo",
                "organization_type": OrganizationType.TRAINING_OFFICE,
                "parent": university,
                "can_write_ledger": True,
                "can_approve": True,
                "is_validator": True,
            },
        )
        faculty, _ = Organization.objects.update_or_create(
            code="FAC-IT",
            defaults={
                "name": "Khoa Công nghệ Thông tin",
                "organization_type": OrganizationType.FACULTY,
                "parent": university,
                "can_write_ledger": True,
                "can_approve": True,
                "is_validator": True,
            },
        )
        department, _ = Organization.objects.update_or_create(
            code="DEP-IS",
            defaults={
                "name": "Bộ môn Hệ thống thông tin",
                "organization_type": OrganizationType.DEPARTMENT,
                "parent": faculty,
                "can_write_ledger": True,
                "can_approve": True,
                "is_validator": True,
            },
        )
        examination, _ = Organization.objects.update_or_create(
            code="EXAM",
            defaults={
                "name": "Phòng Khảo thí",
                "organization_type": OrganizationType.EXAMINATION_OFFICE,
                "parent": university,
                "can_write_ledger": True,
                "can_approve": True,
                "is_validator": True,
            },
        )
        registrar, _ = Organization.objects.update_or_create(
            code="REG",
            defaults={
                "name": "Văn phòng Registrar",
                "organization_type": OrganizationType.REGISTRAR,
                "parent": university,
                "can_write_ledger": True,
                "can_approve": True,
                "is_validator": True,
            },
        )
        qa, _ = Organization.objects.update_or_create(
            code="QA",
            defaults={
                "name": "Phòng Kiểm định QA",
                "organization_type": OrganizationType.QA,
                "parent": university,
                "can_write_ledger": True,
                "can_approve": True,
                "is_validator": True,
            },
        )
        return {
            "university": university,
            "training": training,
            "faculty": faculty,
            "department": department,
            "examination": examination,
            "registrar": registrar,
            "qa": qa,
        }

    def _create_user(self, username, password, role, organization, full_name, email, is_superuser=False):
        user, _ = User.objects.update_or_create(
            username=username,
            defaults={
                "email": email,
                "role": role,
                "full_name": full_name,
                "primary_organization": organization,
                "is_staff": role != UserRole.STUDENT,
                "is_superuser": is_superuser,
            },
        )
        user.set_password(password)
        user.save()
        if organization:
            OrganizationMembership.objects.update_or_create(
                user=user,
                organization=organization,
                role=role,
                defaults={"is_primary": True, "is_active": True},
            )
        return user

    def _seed_users(self, organizations):
        users = {
            "admin": self._create_user(
                "admin",
                "admin12345",
                UserRole.SYSTEM_ADMIN,
                organizations["university"],
                "System Admin",
                "admin@demo-blockchain.edu.vn",
                is_superuser=True,
            ),
            "registrar": self._create_user(
                "registrar",
                "registrar12345",
                UserRole.REGISTRAR,
                organizations["registrar"],
                "Registrar Officer",
                "registrar@demo-blockchain.edu.vn",
            ),
            "faculty": self._create_user(
                "faculty",
                "faculty12345",
                UserRole.FACULTY_ADMIN,
                organizations["faculty"],
                "Faculty Officer",
                "faculty@demo-blockchain.edu.vn",
            ),
            "signer": self._create_user(
                "signer",
                "signer12345",
                UserRole.SIGNER,
                organizations["registrar"],
                "Signing Officer",
                "signer@demo-blockchain.edu.vn",
            ),
            "auditor": self._create_user(
                "auditor",
                "auditor12345",
                UserRole.AUDITOR,
                organizations["qa"],
                "QA Auditor",
                "auditor@demo-blockchain.edu.vn",
            ),
        }
        return users

    def _seed_programs(self, organizations):
        programs = {
            "it": AcademicProgram.objects.update_or_create(
                code="IT",
                defaults={
                    "name": "Công nghệ thông tin",
                    "degree_type": "Bachelor",
                    "total_required_credits": 120,
                    "min_gpa": 2.50,
                    "faculty": organizations["faculty"],
                },
            )[0],
            "is": AcademicProgram.objects.update_or_create(
                code="IS",
                defaults={
                    "name": "Hệ thống thông tin",
                    "degree_type": "Bachelor",
                    "total_required_credits": 120,
                    "min_gpa": 2.50,
                    "faculty": organizations["faculty"],
                },
            )[0],
            "ds": AcademicProgram.objects.update_or_create(
                code="DS",
                defaults={
                    "name": "Khoa học dữ liệu",
                    "degree_type": "Bachelor",
                    "total_required_credits": 125,
                    "min_gpa": 2.70,
                    "faculty": organizations["faculty"],
                },
            )[0],
        }
        return programs

    def _seed_courses(self, programs):
        course_specs = [
            ("BC101", "Blockchain Foundations", 3, programs["it"]),
            ("BC201", "Smart Contract Thinking", 3, programs["it"]),
            ("IS301", "Information Systems Governance", 3, programs["is"]),
            ("DS401", "Data Governance", 3, programs["ds"]),
        ]
        for code, name, credits, program in course_specs:
            Course.objects.update_or_create(
                code=code,
                defaults={"name": name, "credits": credits, "program": program},
            )

    def _create_student_user(self, username, full_name, email):
        user = self._create_user(
            username=username,
            password="student12345",
            role=UserRole.STUDENT,
            organization=None,
            full_name=full_name,
            email=email,
        )
        user.is_staff = False
        user.save(update_fields=["is_staff"])
        return user

    def _seed_students(self, organizations, programs, users):
        studenta_user = self._create_student_user("studenta", "Nguyễn Văn A", "studenta@demo.edu.vn")
        studentb_user = self._create_student_user("studentb", "Trần Thị B", "studentb@demo.edu.vn")

        students = {
            "a": Student.objects.update_or_create(
                student_code="SV001",
                defaults={
                    "full_name": "Nguyễn Văn A",
                    "date_of_birth": "2002-01-10",
                    "email": "studenta@demo.edu.vn",
                    "user": studenta_user,
                    "faculty": organizations["faculty"],
                    "academic_program": programs["it"],
                    "cohort": "K20",
                    "credits_completed": 128,
                    "gpa": 3.40,
                    "graduation_eligible": True,
                    "graduation_status": "Eligible",
                },
            )[0],
            "b": Student.objects.update_or_create(
                student_code="SV002",
                defaults={
                    "full_name": "Trần Thị B",
                    "date_of_birth": "2002-04-14",
                    "email": "studentb@demo.edu.vn",
                    "user": studentb_user,
                    "faculty": organizations["faculty"],
                    "academic_program": programs["is"],
                    "cohort": "K20",
                    "credits_completed": 124,
                    "gpa": 3.10,
                    "graduation_eligible": True,
                    "graduation_status": "Eligible",
                },
            )[0],
            "c": Student.objects.update_or_create(
                student_code="SV003",
                defaults={
                    "full_name": "Lê Minh C",
                    "date_of_birth": "2002-08-22",
                    "email": "studentc@demo.edu.vn",
                    "faculty": organizations["faculty"],
                    "academic_program": programs["it"],
                    "cohort": "K20",
                    "credits_completed": 130,
                    "gpa": 3.55,
                    "graduation_eligible": True,
                    "graduation_status": "Eligible",
                },
            )[0],
            "d": Student.objects.update_or_create(
                student_code="SV004",
                defaults={
                    "full_name": "Phạm Thị D",
                    "date_of_birth": "2003-03-03",
                    "email": "studentd@demo.edu.vn",
                    "faculty": organizations["faculty"],
                    "academic_program": programs["it"],
                    "cohort": "K21",
                    "credits_completed": 90,
                    "gpa": 2.00,
                    "graduation_eligible": False,
                    "graduation_status": "Not eligible",
                },
            )[0],
            "e": Student.objects.update_or_create(
                student_code="SV005",
                defaults={
                    "full_name": "Hoàng Văn E",
                    "date_of_birth": "2003-06-18",
                    "email": "studente@demo.edu.vn",
                    "faculty": organizations["faculty"],
                    "academic_program": programs["ds"],
                    "cohort": "K21",
                    "credits_completed": 125,
                    "gpa": 2.85,
                    "finance_hold": True,
                    "graduation_eligible": False,
                    "graduation_status": "Finance hold",
                },
            )[0],
        }

        for student in students.values():
            for course in Course.objects.filter(program=student.academic_program)[:2]:
                StudentCourseRecord.objects.update_or_create(
                    student=student,
                    course=course,
                    term="HK1",
                    year=2025,
                    defaults={"grade": "A", "passed": True},
                )
        return students

    def _seed_credential_types(self):
        degree_type, _ = CredentialType.objects.update_or_create(
            code="DEGREE",
            defaults={
                "name": "Bằng tốt nghiệp",
                "description": "Bằng tốt nghiệp đại học",
                "default_validity_type": "Permanent",
                "public_fields_json": ["owner_name", "issuer_name", "issued_at", "serial_number"],
                "allow_public_pdf": True,
            },
        )
        blockchain_type, _ = CredentialType.objects.update_or_create(
            code="BLOCKCHAIN_CERT",
            defaults={
                "name": "Chứng chỉ hoàn thành khóa học blockchain",
                "description": "Certificate of blockchain short-course completion",
                "default_validity_type": "Permanent",
                "public_fields_json": ["owner_name", "issuer_name", "issued_at", "serial_number"],
                "allow_public_pdf": True,
            },
        )
        completion_type, _ = CredentialType.objects.update_or_create(
            code="COMPLETION",
            defaults={
                "name": "Giấy xác nhận hoàn thành chương trình",
                "description": "Completion confirmation",
                "default_validity_type": "Permanent",
                "public_fields_json": ["owner_name", "issuer_name", "issued_at", "serial_number"],
                "allow_public_pdf": False,
            },
        )
        templates = {
            "degree": CredentialTemplate.objects.update_or_create(
                code="TPL-DEGREE-V1",
                defaults={"name": "Mẫu bằng tốt nghiệp", "credential_type": degree_type, "version": "1.0"},
            )[0],
            "blockchain": CredentialTemplate.objects.update_or_create(
                code="TPL-BC-V1",
                defaults={"name": "Mẫu chứng chỉ blockchain", "credential_type": blockchain_type, "version": "1.0"},
            )[0],
            "completion": CredentialTemplate.objects.update_or_create(
                code="TPL-COMP-V1",
                defaults={"name": "Mẫu giấy xác nhận", "credential_type": completion_type, "version": "1.0"},
            )[0],
        }
        return {
            "degree": degree_type,
            "blockchain": blockchain_type,
            "completion": completion_type,
        }, templates

    def _seed_policy_rules(self):
        policy_specs = [
            (
                "RULE-CREDITS",
                "Completed required credits",
                {
                    "operator": "AND",
                    "conditions": [
                        {
                            "source": "student",
                            "field": "credits_completed",
                            "op": "gte",
                            "value_from": "program.total_required_credits",
                        }
                    ],
                },
            ),
            (
                "RULE-GPA",
                "Minimum GPA",
                {
                    "operator": "AND",
                    "conditions": [
                        {
                            "source": "student",
                            "field": "gpa",
                            "op": "gte",
                            "value_from": "program.min_gpa",
                        }
                    ],
                },
            ),
            (
                "RULE-FINANCE",
                "Finance clearance",
                {
                    "operator": "AND",
                    "conditions": [
                        {"source": "student", "field": "finance_hold", "op": "eq", "value": False}
                    ],
                },
            ),
            (
                "RULE-DISCIPLINE",
                "Discipline clearance",
                {
                    "operator": "AND",
                    "conditions": [
                        {"source": "student", "field": "discipline_hold", "op": "eq", "value": False}
                    ],
                },
            ),
        ]
        for index, (code, name, expression) in enumerate(policy_specs, start=1):
            PolicyRule.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "description": name,
                    "rule_type": "ELIGIBILITY",
                    "expression_json": expression,
                    "priority": index * 10,
                    "active": True,
                },
            )

    def _ensure_signing_key(self, registrar_org):
        private_key_path = Path(settings.MEDIA_ROOT) / "keys" / "demo_registrar_private.pem"
        if not private_key_path.exists():
            public_key_pem = generate_rsa_key_pair(str(private_key_path))
        else:
            public_key_pem = generate_rsa_key_pair(str(private_key_path))
        signing_key, _ = SigningKey.objects.update_or_create(
            organization=registrar_org,
            key_name="Demo Registrar Key",
            defaults={
                "algorithm": "RSA",
                "public_key_pem": public_key_pem,
                "private_key_reference": str(private_key_path),
                "active": True,
            },
        )
        return signing_key

    def _approve_full_flow(self, request_obj, users):
        evaluate_eligibility_rules(request_obj, actor_user=users["faculty"])
        run_approval_step(request_obj, ApprovalStepType.ACADEMIC, users["faculty"], True, "Eligible by faculty")
        run_approval_step(request_obj, ApprovalStepType.EXAMINATION, users["admin"], True, "Exam data verified")
        run_approval_step(request_obj, ApprovalStepType.FINANCE, users["admin"], True, "Finance cleared")
        run_approval_step(request_obj, ApprovalStepType.DISCIPLINE, users["auditor"], True, "Discipline cleared")
        run_approval_step(request_obj, ApprovalStepType.REGISTRAR, users["registrar"], True, "Final approval")

    def _build_published_credential(self, student, credential_type, template, users, signing_key, note):
        request_obj = create_issuance_request(
            student=student,
            credential_type=credential_type,
            template=template,
            requested_by=users["faculty"],
            notes=note,
        )
        self._approve_full_flow(request_obj, users)
        credential = issue_credential_from_request(request_obj, users["registrar"])
        sign_credential(credential, signing_key, users["signer"], signer_title="Certificate Authority Officer")
        publish_credential(credential, users["registrar"])
        return credential

    def _seed_demo_flows(self, users, students, credential_types, templates, signing_key):
        self._build_published_credential(
            student=students["a"],
            credential_type=credential_types["degree"],
            template=templates["degree"],
            users=users,
            signing_key=signing_key,
            note="Valid credential demo",
        )

        revoked_credential = self._build_published_credential(
            student=students["b"],
            credential_type=credential_types["blockchain"],
            template=templates["blockchain"],
            users=users,
            signing_key=signing_key,
            note="Revoked credential demo",
        )
        revoke_credential(
            revoked_credential,
            actor_user=users["auditor"],
            reason="Fraud detected in supporting document",
            decision_number="QD-TH-2026-001",
            public_note="Credential has been revoked by QA office.",
        )

        superseded_source = self._build_published_credential(
            student=students["c"],
            credential_type=credential_types["completion"],
            template=templates["completion"],
            users=users,
            signing_key=signing_key,
            note="Superseded credential demo",
        )
        supersede_credential(
            superseded_source,
            actor_user=users["registrar"],
            corrected_payload_updates={"student": {"full_name": "Lê Minh C (Corrected)"}},
            notes="Corrected typo in student name.",
        )

        fail_request = create_issuance_request(
            student=students["d"],
            credential_type=credential_types["degree"],
            template=templates["degree"],
            requested_by=users["faculty"],
            notes="Should fail due to insufficient credits and GPA.",
        )
        evaluate_eligibility_rules(fail_request, actor_user=users["faculty"])

        hold_request = create_issuance_request(
            student=students["e"],
            credential_type=credential_types["degree"],
            template=templates["degree"],
            requested_by=users["faculty"],
            notes="Should fail due to finance hold.",
        )
        evaluate_eligibility_rules(hold_request, actor_user=users["faculty"])
