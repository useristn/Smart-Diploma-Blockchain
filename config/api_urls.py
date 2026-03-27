from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import include, path

from accounts.views import MembershipViewSet, UserViewSet
from academics.views import AcademicProgramViewSet, CourseViewSet
from audit.views import AuditLogViewSet
from credentials.views import CredentialTypeViewSet, CredentialViewSet
from issuance.views import ApprovalStepViewSet, IssuanceRequestViewSet
from ledger.views import LedgerEventViewSet
from organizations.views import OrganizationViewSet
from policy_engine.views import PolicyEvaluationViewSet, PolicyRuleViewSet
from reports.views import ReportSummaryView
from students.views import StudentViewSet, StudentCourseRecordViewSet
from verification.views import VerificationLookupView


router = DefaultRouter()
router.register("users", UserViewSet, basename="api-users")
router.register("memberships", MembershipViewSet, basename="api-memberships")
router.register("organizations", OrganizationViewSet, basename="api-organizations")
router.register("programs", AcademicProgramViewSet, basename="api-programs")
router.register("courses", CourseViewSet, basename="api-courses")
router.register("students", StudentViewSet, basename="api-students")
router.register(
    "student-course-records",
    StudentCourseRecordViewSet,
    basename="api-student-course-records",
)
router.register(
    "issuance-requests",
    IssuanceRequestViewSet,
    basename="api-issuance-requests",
)
router.register("approvals", ApprovalStepViewSet, basename="api-approvals")
router.register("credentials", CredentialViewSet, basename="api-credentials")
router.register(
    "credential-types", CredentialTypeViewSet, basename="api-credential-types"
)
router.register("policy-rules", PolicyRuleViewSet, basename="api-policy-rules")
router.register(
    "policy-evaluations",
    PolicyEvaluationViewSet,
    basename="api-policy-evaluations",
)
router.register("ledger-events", LedgerEventViewSet, basename="api-ledger-events")
router.register("audit-logs", AuditLogViewSet, basename="api-audit-logs")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verification/lookup/", VerificationLookupView.as_view(), name="api-verify"),
    path("reports/summary/", ReportSummaryView.as_view(), name="api-report-summary"),
]
