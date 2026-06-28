from django.db import models
from accounts.models import User


class CalendarEvent(models.Model):
    EVENT_FEAST = 'feast'
    EVENT_FAST = 'fast'
    EVENT_CLASS = 'class'
    EVENT_MEZMUR = 'mezmur'
    EVENT_PARENT_MEETING = 'parent_meeting'
    EVENT_COMPETITION = 'competition'
    EVENT_OTHER = 'other'

    EVENT_TYPE_CHOICES = [
        (EVENT_FEAST, 'Feast'),
        (EVENT_FAST, 'Fast'),
        (EVENT_CLASS, 'Class'),
        (EVENT_MEZMUR, 'Mezmur Practice'),
        (EVENT_PARENT_MEETING, 'Parent Meeting'),
        (EVENT_COMPETITION, 'Bible Competition'),
        (EVENT_OTHER, 'Other'),
    ]

    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default=EVENT_OTHER)
    is_recurring = models.BooleanField(default=False)
    is_orthodox_calendar_event = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'title']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['event_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.start_date}"
