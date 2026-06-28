from django.contrib import admin
from .models import Assignment, AssignmentSubmission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_level', 'teacher', 'due_date', 'is_published', 'created_at')
    list_filter = ('class_level', 'is_published', 'due_date')
    search_fields = ('title', 'description')


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('assignment__title', 'student__full_name')
