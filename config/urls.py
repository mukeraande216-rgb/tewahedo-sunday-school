from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts.views import role_based_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', role_based_dashboard, name='dashboard'),
    path('students/', include('students.urls')),
    path('classes/', include('classes.urls')),
    path('assignments/', include('assignments.urls')),
    path('attendance/', include('attendance.urls')),
    path('announcements/', include('announcements.urls')),
    path('resources/', include('resources.urls')),
    path('calendar/', include('calendar_app.urls')),
    path('reports/', include('reports.urls')),
    path('messaging/', include('messaging.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
