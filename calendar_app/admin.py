from django.contrib import admin
from .models import CalendarEvent


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'event_type', 'is_orthodox_calendar_event')
    list_filter = ('event_type', 'is_recurring', 'is_orthodox_calendar_event')
    search_fields = ('title', 'description')
