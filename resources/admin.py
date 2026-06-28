from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'class_level',
        'is_published',
        'uploaded_by',
        'created_at',
    ]

    list_filter = [
        'class_level',
        'is_published',
        'created_at',
    ]

    search_fields = [
        'title',
        'description',
        'youtube_link',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]