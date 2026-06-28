from django import forms
from .models import ProgressReport


class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ['student', 'period', 'attendance_rate', 'homework_completion', 'participation', 'memory_verses', 'prayer_memorization', 'mezmur_participation', 'behavior_respect', 'church_service_participation', 'teacher_comments', 'parent_notes', 'created_by']
