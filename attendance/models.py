from django.db import models
from accounts.models import User
from students.models import Student


class Attendance(models.Model):
    STATUS_PRESENT = 'present'
    STATUS_ABSENT = 'absent'
    STATUS_LATE = 'late'
    STATUS_EXCUSED = 'excused'

    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_ABSENT, 'Absent'),
        (STATUS_LATE, 'Late'),
        (STATUS_EXCUSED, 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    session_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, limit_choices_to={'role': 'teacher'}, null=True, blank=True, on_delete=models.SET_NULL, related_name='marked_attendance')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'session_date'], name='unique_attendance_per_student_date')
        ]
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['session_date']),
            models.Index(fields=['status']),
        ]
        ordering = ['-session_date']

    def __str__(self):
        return f"{self.student} - {self.session_date} - {self.get_status_display()}"
