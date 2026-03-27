from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("tai-khoan/", include("accounts.urls")),
    path("to-chuc/", include("organizations.urls")),
    path("hoc-vu/", include("academics.urls")),
    path("sinh-vien/", include("students.urls")),
    path("cap-phat/", include("issuance.urls")),
    path("chinh-sach/", include("policy_engine.urls")),
    path("chung-chi/", include("credentials.urls")),
    path("so-cai/", include("ledger.urls")),
    path("kiem-toan/", include("audit.urls")),
    path("bao-cao/", include("reports.urls")),
    path("xac-thuc/", include("public_portal.urls")),
    path("api/", include("config.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
