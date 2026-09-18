from django.core.management.base import BaseCommand

from ejercicios.models import Ejercicio


class Command(BaseCommand):
    help = "Asigna una imagen local de respaldo a ejercicios sin GIF ni imagen."

    def handle(self, *args, **options):
        updated = Ejercicio.objects.filter(gif_url="", imagen_url="").update(
            imagen_url="/static/img/exercise-placeholder.svg"
        )
        self.stdout.write(
            self.style.SUCCESS(f"Medios completados para {updated} ejercicios.")
        )
