import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = (
        "Create a superuser from environment variables ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD "
        "if it does not already exist. Useful for non-interactive provisioning in production."
    )

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("ADMIN_USERNAME")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not (username and email and password):
            self.stdout.write(self.style.WARNING(
                "ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD must be set to create a default superuser. Skipping."
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.NOTICE if hasattr(self.style, 'NOTICE') else self.style.WARNING(
                f"Superuser with username '{username}' already exists."
            ))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully."))
