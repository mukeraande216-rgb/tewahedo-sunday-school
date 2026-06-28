from django.contrib import admin
from .models import ProgressReport


@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'period', 'attendance_rate', 'homework_completion', 'generated_at')
    list_filter = ('period', 'generated_at')
    search_fields = ('student__full_name', 'teacher_comments')
