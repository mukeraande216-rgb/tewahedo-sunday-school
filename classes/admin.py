from django.contrib import admin
from .models import ClassLevel, ClassEnrollment, ClassGroup


@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(ClassEnrollment)
class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_level', 'teacher', 'is_active', 'enrollment_date')
    list_filter = ('class_level', 'is_active')
    search_fields = ('student__full_name',)


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_level', 'created_at')
    list_filter = ('class_level',)
    search_fields = ('name',)
