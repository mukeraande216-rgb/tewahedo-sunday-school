from django.db import models
from accounts.models import User
from students.models import Student


class ProgressReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_reports')
    period = models.CharField(max_length=50)
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    homework_completion = models.PositiveIntegerField(default=0)
    participation = models.PositiveIntegerField(default=0)
    memory_verses = models.PositiveIntegerField(default=0)
    prayer_memorization = models.PositiveIntegerField(default=0)
    mezmur_participation = models.PositiveIntegerField(default=0)
    behavior_respect = models.PositiveIntegerField(default=0)
    church_service_participation = models.PositiveIntegerField(default=0)
    teacher_comments = models.TextField(blank=True)
    parent_notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, limit_choices_to={'role': 'teacher'}, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_progress_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'period'], name='unique_progress_report_per_student_period')
        ]
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['period']),
            models.Index(fields=['generated_at']),
        ]

    def __str__(self):
        return f"{self.student} - {self.period}"
