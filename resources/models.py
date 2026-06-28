from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User
from classes.models import ClassLevel


def validate_resource_file(file):
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

    max_size_mb = 30

    file_name = file.name.lower()
    extension = file_name.split('.')[-1]

    if extension not in allowed_extensions:
        raise ValidationError(
            'Unsupported file type. Allowed files: PDF, Word, Excel, PowerPoint, TXT, CSV, images, audio, and video.'
        )

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'File size cannot exceed {max_size_mb} MB.')


def validate_youtube_url(value):
    if value and ('youtube.com' not in value and 'youtu.be' not in value):
        raise ValidationError('Enter a valid YouTube URL.')


class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class_level = models.ForeignKey(
        ClassLevel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='resources'
    )

    file = models.FileField(
        upload_to='resources/files/',
        blank=True,
        validators=[validate_resource_file]
    )

    youtube_link = models.URLField(
        blank=True,
        validators=[validate_youtube_url]
    )

    is_published = models.BooleanField(default=True)

    uploaded_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='uploaded_resources'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.file and not self.youtube_link:
            raise ValidationError('Please upload a file or add a YouTube link.')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['class_level']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title