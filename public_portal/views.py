from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from verification.services import build_public_verification_context, resolve_credential_lookup, verify_lookup

from public_portal.forms import VerificationSearchForm

_THROTTLE_RATE = 30  # max requests
_THROTTLE_WINDOW = 60  # seconds


def _check_throttle(request) -> bool:
    """Return True if request is within rate limit, False if throttled."""
    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "unknown"))
    ip = ip.split(",")[0].strip()
    cache_key = f"public_verif_throttle:{ip}"
    count = cache.get(cache_key, 0)
    if count >= _THROTTLE_RATE:
        return False
    cache.set(cache_key, count + 1, timeout=_THROTTLE_WINDOW)
    return True


class PublicVerificationHomeView(TemplateView):
    template_name = "public_portal/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = VerificationSearchForm()
        return context

    def post(self, request, *args, **kwargs):
        if not _check_throttle(request):
            return HttpResponse(
                "Quá nhiều yêu cầu. Vui lòng thử lại sau.",
                status=429,
                content_type="text/plain; charset=utf-8",
            )
        form = VerificationSearchForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        value = form.cleaned_data["lookup_value"]
        credential = resolve_credential_lookup(value)
        if not credential:
            return render(
                request,
                self.template_name,
                {"form": form, "lookup_error": "Không tìm thấy chứng chỉ phù hợp."},
            )
        return redirect("public_portal:detail", slug=credential.public_slug)


class PublicVerificationDetailView(TemplateView):
    template_name = "public_portal/detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not _check_throttle(request):
            return HttpResponse(
                "Quá nhiều yêu cầu. Vui lòng thử lại sau.",
                status=429,
                content_type="text/plain; charset=utf-8",
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        credential, verify_context = verify_lookup(
            self.request,
            self.kwargs["slug"],
            method="PUBLIC_SLUG",
        )
        context["credential"] = credential
        context["verify_context"] = verify_context
        return context
