from django.contrib import admin
from .models import Parent, Student


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'emergency_contact', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'parent', 'gender', 'is_active', 'registration_approved', 'created_at')
    list_filter = ('gender', 'is_active', 'registration_approved')
    search_fields = ('full_name', 'parent__user__username', 'parent__user__email')
