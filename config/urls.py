from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from accounts.views import role_based_dashboard


urlpatterns = [
    path("admin/", admin.site.urls),

    # Language selector
    path("i18n/", include("django.conf.urls.i18n")),

    # Existing Sunday School system
    path("accounts/", include("accounts.urls")),
    path("dashboard/", role_based_dashboard, name="dashboard"),
    path("students/", include("students.urls")),
    path("classes/", include("classes.urls")),
    path("assignments/", include("assignments.urls")),
    path("attendance/", include("attendance.urls")),
    path("announcements/", include("announcements.urls")),
    path("resources/", include("resources.urls")),
    path("calendar/", include("calendar_app.urls")),
    path("reports/", include("reports.urls")),
    path("messaging/", include("messaging.urls")),

    # Private church membership management
    path("membership/", include("membership.urls")),

    # Serve uploaded files such as homework attachments and submissions
    path(
        "media/<path:path>",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),

    # Public church website
    path("", include("website.urls")),
]