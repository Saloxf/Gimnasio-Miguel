import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea o actualiza un administrador usando variables de entorno."

    def handle(self, *args, **options):
        username = os.environ.get("FITTRACK_ADMIN_USERNAME")
        email = os.environ.get("FITTRACK_ADMIN_EMAIL")
        password = os.environ.get("FITTRACK_ADMIN_PASSWORD")
        if not all((username, email, password)):
            raise CommandError(
                "Define FITTRACK_ADMIN_USERNAME, FITTRACK_ADMIN_EMAIL y "
                "FITTRACK_ADMIN_PASSWORD antes de ejecutar el comando."
            )
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
        action = "creado" if created else "actualizado"
        self.stdout.write(self.style.SUCCESS(f"Administrador {action}: {username}"))
