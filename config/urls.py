from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

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

    # Serve uploaded files such as homework attachments and submissions.
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]