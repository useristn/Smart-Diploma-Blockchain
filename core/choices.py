from django.db import models


class OrganizationType(models.TextChoices):
    UNIVERSITY = "UNIVERSITY", "Trường đại học"
    FACULTY = "FACULTY", "Khoa"
    DEPARTMENT = "DEPARTMENT", "Bộ môn"
    TRAINING_OFFICE = "TRAINING_OFFICE", "Phòng đào tạo"
    EXAMINATION_OFFICE = "EXAMINATION_OFFICE", "Phòng khảo thí"
    REGISTRAR = "REGISTRAR", "Văn phòng registrar"
    QA = "QA", "Đơn vị QA"
    PARTNER = "PARTNER", "Đối tác"


class UserRole(models.TextChoices):
    SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Admin"
    UNIVERSITY_ADMIN = "UNIVERSITY_ADMIN", "University Admin"
    REGISTRAR = "REGISTRAR", "Registrar"
    FACULTY_ADMIN = "FACULTY_ADMIN", "Faculty Admin"
    DEPARTMENT_OFFICER = "DEPARTMENT_OFFICER", "Department Officer"
    EXAMINATION_OFFICER = "EXAMINATION_OFFICER", "Examination Officer"
    ACADEMIC_ADVISOR = "ACADEMIC_ADVISOR", "Academic Advisor"
    SIGNER = "SIGNER", "Signer"
    AUDITOR = "AUDITOR", "Auditor / QA"
    STUDENT = "STUDENT", "Student"
    ORGANIZATION_STAFF = "ORGANIZATION_STAFF", "Organization Staff"


class StudentStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Đang học"
    GRADUATED = "GRADUATED", "Đã tốt nghiệp"
    SUSPENDED = "SUSPENDED", "Tạm ngưng"
    INACTIVE = "INACTIVE", "Không hoạt động"


class IssuanceRequestStatus(models.TextChoices):
    SUBMITTED = "SUBMITTED", "Đã nộp"
    UNDER_REVIEW = "UNDER_REVIEW", "Đang rà soát"
    ACADEMIC_ELIGIBLE = "ACADEMIC_ELIGIBLE", "Đủ điều kiện học vụ"
    FINANCE_CLEARED = "FINANCE_CLEARED", "Đã qua tài chính"
    DISCIPLINE_CLEARED = "DISCIPLINE_CLEARED", "Đã qua kỷ luật"
    FINAL_APPROVED = "FINAL_APPROVED", "Phê duyệt cuối"
    SIGNED = "SIGNED", "Đã ký"
    PUBLISHED = "PUBLISHED", "Đã công bố"
    REJECTED = "REJECTED", "Từ chối"
    REVOKED = "REVOKED", "Đã thu hồi"
    SUPERSEDED = "SUPERSEDED", "Đã thay thế"


class ApprovalStepType(models.TextChoices):
    ACADEMIC = "ACADEMIC", "Học vụ"
    EXAMINATION = "EXAMINATION", "Khảo thí"
    FINANCE = "FINANCE", "Tài chính"
    DISCIPLINE = "DISCIPLINE", "Kỷ luật"
    REGISTRAR = "REGISTRAR", "Registrar"
    SIGN_OFF = "SIGN_OFF", "Cho phép ký"


class ApprovalStatus(models.TextChoices):
    PENDING = "PENDING", "Chờ xử lý"
    APPROVED = "APPROVED", "Đã duyệt"
    REJECTED = "REJECTED", "Từ chối"


class CredentialStatus(models.TextChoices):
    DRAFT = "DRAFT", "Nháp"
    ISSUED = "ISSUED", "Đã cấp"
    SIGNED = "SIGNED", "Đã ký"
    PUBLISHED = "PUBLISHED", "Đã công bố"
    SUSPENDED = "SUSPENDED", "Tạm đình chỉ"
    REVOKED = "REVOKED", "Đã thu hồi"
    SUPERSEDED = "SUPERSEDED", "Đã thay thế"


class PolicyRuleType(models.TextChoices):
    ELIGIBILITY = "ELIGIBILITY", "Điều kiện cấp"
    PUBLISHING = "PUBLISHING", "Điều kiện publish"
    REVOCATION = "REVOCATION", "Điều kiện thu hồi"


class VerificationMethod(models.TextChoices):
    QR = "QR", "QR"
    CODE = "CODE", "Verification Code"
    CREDENTIAL_CODE = "CREDENTIAL_CODE", "Credential Code"
    PUBLIC_SLUG = "PUBLIC_SLUG", "Public Slug"


class LedgerEventType(models.TextChoices):
    STUDENT_REGISTERED = "STUDENT_REGISTERED", "Student registered"
    PROGRAM_ASSIGNED = "PROGRAM_ASSIGNED", "Program assigned"
    ISSUANCE_REQUEST_CREATED = "ISSUANCE_REQUEST_CREATED", "Issuance request created"
    ELIGIBILITY_CHECK_PASSED = "ELIGIBILITY_CHECK_PASSED", "Eligibility check passed"
    ELIGIBILITY_CHECK_FAILED = "ELIGIBILITY_CHECK_FAILED", "Eligibility check failed"
    APPROVAL_GRANTED = "APPROVAL_GRANTED", "Approval granted"
    APPROVAL_REJECTED = "APPROVAL_REJECTED", "Approval rejected"
    CREDENTIAL_ISSUED = "CREDENTIAL_ISSUED", "Credential issued"
    PDF_RENDERED = "PDF_RENDERED", "PDF rendered"
    CREDENTIAL_SIGNED = "CREDENTIAL_SIGNED", "Credential signed"
    CREDENTIAL_PUBLISHED = "CREDENTIAL_PUBLISHED", "Credential published"
    CREDENTIAL_VERIFIED = "CREDENTIAL_VERIFIED", "Credential verified"
    CREDENTIAL_REVOKED = "CREDENTIAL_REVOKED", "Credential revoked"
    CREDENTIAL_SUSPENDED = "CREDENTIAL_SUSPENDED", "Credential suspended"
    CREDENTIAL_SUPERSEDED = "CREDENTIAL_SUPERSEDED", "Credential superseded"
    CHAIN_VERIFIED = "CHAIN_VERIFIED", "Chain verified"
    BATCH_COMMITTED = "BATCH_COMMITTED", "Batch committed (Merkle)"
