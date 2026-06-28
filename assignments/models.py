from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from accounts.models import User
from classes.models import ClassLevel


def validate_youtube_url(value):
    if value and ('youtube.com' not in value and 'youtu.be' not in value):
        raise ValidationError('Enter a valid YouTube URL.')


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(User, limit_choices_to={'role': 'teacher'}, on_delete=models.CASCADE, related_name='assignments')
    youtube_link = models.URLField(blank=True, validators=[validate_youtube_url])
    attachment = models.FileField(upload_to='assignments/', blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['class_level']),
            models.Index(fields=['teacher']),
            models.Index(fields=['due_date']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    STATUS_NOT_SUBMITTED = 'not_submitted'
    STATUS_SUBMITTED = 'submitted'
    STATUS_COMPLETE = 'complete'
    STATUS_INCOMPLETE = 'incomplete'
    STATUS_LATE = 'late'
    STATUS_NEEDS_CORRECTION = 'needs_correction'

    STATUS_CHOICES = [
        (STATUS_NOT_SUBMITTED, 'Not submitted'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_INCOMPLETE, 'Incomplete'),
        (STATUS_LATE, 'Late'),
        (STATUS_NEEDS_CORRECTION, 'Needs correction'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='assignment_submissions')
    response_text = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/', blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_NOT_SUBMITTED)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_submissions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['assignment', 'student'], name='unique_submission_per_assignment_student')
        ]
        indexes = [
            models.Index(fields=['assignment']),
            models.Index(fields=['student']),
            models.Index(fields=['status']),
            models.Index(fields=['submitted_at']),
        ]

    def save(self, *args, **kwargs):
        if self.status == self.STATUS_SUBMITTED and self.submitted_at is None:
            self.submitted_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.assignment} ({self.get_status_display()})"
