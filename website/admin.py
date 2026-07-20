from django.contrib import admin

from .models import (
    Announcement,
    ClergyMember,
    ContactSubmission,
    Event,
    Ministry,
    SacramentalRequest,
    Sermon,
    ServiceSchedule,
    SiteSettings,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": (
            "church_name_en", "church_name_am", "short_name",
            "motto_en", "motto_am", "welcome_en", "welcome_am",
        )}),
        ("Contact", {"fields": ("address", "phone", "email", "office_hours", "map_url")}),
        ("Online services", {"fields": (
            "livestream_url", "youtube_url", "facebook_url", "instagram_url",
            "donation_url", "sunday_school_url",
        )}),
        ("Appearance", {"fields": ("hero_image_url",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title_en", "priority", "starts_at", "ends_at", "is_published")
    list_filter = ("priority", "is_published")
    search_fields = ("title_en", "title_am", "body_en", "body_am")


@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = ("name_en", "day_of_week", "start_time", "end_time", "is_featured", "is_active")
    list_filter = ("day_of_week", "is_featured", "is_active")
    list_editable = ("is_featured", "is_active")


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ("name_en", "audience_en", "is_featured", "is_active", "sort_order")
    list_filter = ("is_featured", "is_active")
    list_editable = ("is_featured", "is_active", "sort_order")
    prepopulated_fields = {"slug": ("name_en",)}
    search_fields = ("name_en", "name_am", "summary_en", "summary_am")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title_en", "start_at", "end_at", "location", "is_featured", "is_published")
    list_filter = ("is_featured", "is_published")
    search_fields = ("title_en", "title_am", "description_en", "description_am", "location")
    date_hierarchy = "start_at"


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ("title_en", "speaker", "preached_on", "language", "is_published")
    list_filter = ("language", "is_published")
    search_fields = ("title_en", "title_am", "speaker", "scripture_reference")
    date_hierarchy = "preached_on"


@admin.register(ClergyMember)
class ClergyMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "title_en", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")


@admin.register(SacramentalRequest)
class SacramentalRequestAdmin(admin.ModelAdmin):
    list_display = ("requester_name", "service_type", "preferred_date", "status", "created_at")
    list_filter = ("service_type", "status")
    search_fields = ("requester_name", "email", "phone")
    readonly_fields = ("created_at",)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "created_at", "is_resolved")
    list_filter = ("is_resolved",)
    list_editable = ("is_resolved",)
    search_fields = ("subject", "name", "email", "message")
    readonly_fields = ("created_at",)
