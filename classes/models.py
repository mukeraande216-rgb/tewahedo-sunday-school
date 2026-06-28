from django.db import models
from accounts.models import User


class ClassLevel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    teachers = models.ManyToManyField(User, blank=True, related_name='assigned_class_levels', limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.name


class ClassEnrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='enrollments')
    teacher = models.ForeignKey(User, limit_choices_to={'role': 'teacher'}, null=True, blank=True, on_delete=models.SET_NULL, related_name='class_enrollments')
    is_active = models.BooleanField(default=True)
    enrollment_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'class_level'], name='unique_student_class_enrollment')
        ]
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['class_level']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.student} - {self.class_level}"


class ClassGroup(models.Model):
    name = models.CharField(max_length=100)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='groups')
    students = models.ManyToManyField('students.Student', blank=True, related_name='class_groups')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'class_level'], name='unique_group_per_class')
        ]

    def __str__(self):
        return f"{self.name} ({self.class_level})"
