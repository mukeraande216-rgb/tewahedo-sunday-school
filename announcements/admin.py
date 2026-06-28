from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'target', 'class_level', 'is_published', 'created_by', 'created_at')
    list_filter = ('target', 'class_level', 'is_published')
    search_fields = ('title', 'content')
