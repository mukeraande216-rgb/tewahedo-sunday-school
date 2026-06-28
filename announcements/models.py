from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import User
from classes.models import ClassLevel


def validate_youtube_url(value):
    if value and ('youtube.com' not in value and 'youtu.be' not in value):
        raise ValidationError('Enter a valid YouTube URL.')


def validate_announcement_attachment(file):
    allowed_extensions = [
        'pdf',
        'doc',
        'docx',
        'xls',
        'xlsx',
        'ppt',
        'pptx',
        'txt',
        'csv',
        'jpg',
        'jpeg',
        'png',
        'gif',
        'mp3',
        'mp4',
        'wav',
        'm4a',
    ]

    max_size_mb = 20

    file_name = file.name.lower()
    extension = file_name.split('.')[-1]

    if extension not in allowed_extensions:
        raise ValidationError(
            'Unsupported file type. Allowed files: PDF, Word, Excel, PowerPoint, TXT, CSV, images, audio, and video.'
        )

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size cannot exceed {max_size_mb} MB.')


class Announcement(models.Model):
    TARGET_ALL = 'all'
    TARGET_CLASS = 'class'

    TARGET_CHOICES = [
        (TARGET_ALL, 'All'),
        (TARGET_CLASS, 'Class'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default=TARGET_ALL)
    class_level = models.ForeignKey(
        ClassLevel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='announcements'
    )
    image = models.ImageField(upload_to='announcements/images/', blank=True)
    attachment = models.FileField(
        upload_to='announcements/files/',
        blank=True,
        validators=[validate_announcement_attachment]
    )
    youtube_link = models.URLField(blank=True, validators=[validate_youtube_url])
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='announcements'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.target == self.TARGET_CLASS and self.class_level is None:
            raise ValidationError('Class-level announcements require a class level.')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target']),
            models.Index(fields=['class_level']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title