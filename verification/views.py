from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.throttles import PublicVerificationThrottle
from verification.services import build_public_verification_context, resolve_credential_lookup


class VerificationLookupView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PublicVerificationThrottle]

    def get(self, request, *args, **kwargs):
        value = request.GET.get("value", "").strip()
        if not value:
            return Response({"detail": "Thiếu giá trị tra cứu."}, status=400)
        credential = resolve_credential_lookup(value)
        if not credential:
            return Response({"detail": "Không tìm thấy chứng chỉ."}, status=404)
        context = build_public_verification_context(credential)
        return Response(
            {
                "credential_code": credential.credential_code,
                "verification_code": credential.verification_code,
                "status": context["public_status"],
                "owner_name": context["owner_name"],
                "issuer_name": context["issuer_name"],
                "signature_valid": context["signature_valid"],
                "ledger_valid": context["ledger_valid"],
            }
        )

# Create your views here.
