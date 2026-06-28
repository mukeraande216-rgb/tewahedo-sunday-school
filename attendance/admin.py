from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session_date', 'status', 'marked_by')
    list_filter = ('status', 'session_date')
    search_fields = ('student__full_name',)
