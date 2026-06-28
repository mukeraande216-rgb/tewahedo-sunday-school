from django.db import models

from accounts.models import User


class MessageThread(models.Model):
    subject = models.CharField(max_length=200)
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='parent_message_threads'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_message_threads'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_message_threads'
    )
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.subject


class MessageReply(models.Model):
    thread = models.ForeignKey(
        MessageThread,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_message_replies'
    )
    body = models.TextField()
    attachment = models.FileField(
        upload_to='messages/attachments/',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} - {self.created_at}'