import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the initial superuser from environment variables if it does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Superuser environment variables are missing. Skipping superuser creation.'
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" already exists. Skipping creation.'
                )
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        user.role = 'admin'
        user.is_approved = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{username}" created successfully.'
            )
        )