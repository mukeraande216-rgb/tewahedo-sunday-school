from django.contrib import admin

from .models import MessageReply, MessageThread


class MessageReplyInline(admin.TabularInline):
    model = MessageReply
    extra = 0


@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    list_display = [
        'subject',
        'parent',
        'teacher',
        'is_closed',
        'created_at',
        'updated_at',
    ]
    list_filter = [
        'is_closed',
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'subject',
        'parent__username',
        'teacher__username',
    ]
    inlines = [MessageReplyInline]


@admin.register(MessageReply)
class MessageReplyAdmin(admin.ModelAdmin):
    list_display = [
        'thread',
        'sender',
        'created_at',
    ]
    search_fields = [
        'body',
        'sender__username',
        'thread__subject',
    ]