from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils.text import slugify

from ejercicios.models import Ejercicio, GrupoMuscular
from rutinas.models import EjercicioDePlantilla, PlantillaRutina


TEMPLATES = [
    ("ganancia_muscular", "Hipertrofia de pecho", "Pecho", ["press", "fly", "push"], 4, 10),
    ("ganancia_muscular", "Hipertrofia de espalda", "Espalda", ["remo", "pull", "lat"], 4, 10),
    ("ganancia_muscular", "Hipertrofia de piernas", "Piernas", ["sentadilla", "leg", "lunge"], 4, 10),
    ("fuerza", "Fuerza de pecho y hombros", "Pecho", ["bench press", "press", "military"], 5, 5),
    ("fuerza", "Fuerza de espalda", "Espalda", ["deadlift", "remo", "row", "pull"], 5, 5),
    ("fuerza", "Fuerza de piernas", "Piernas", ["squat", "sentadilla", "deadlift", "lunge"], 5, 5),
    ("perdida_grasa", "Quema activa de tren superior", "Pecho", ["push", "burpee", "mountain", "jump"], 3, 12),
    ("perdida_grasa", "Quema activa de espalda", "Espalda", ["row", "remo", "pull", "jump"], 3, 12),
    ("perdida_grasa", "Quema activa de piernas", "Piernas", ["squat", "jump", "lunge", "salto"], 3, 12),
    ("condicion_fisica", "Condición de tren superior", "Pecho", ["push", "press", "plank"], 3, 12),
    ("condicion_fisica", "Condición de espalda", "Espalda", ["row", "remo", "pull", "plank"], 3, 12),
    ("condicion_fisica", "Condición de piernas", "Piernas", ["squat", "lunge", "jump", "plank"], 3, 12),
    ("mantenimiento", "Mantenimiento de pecho", "Pecho", ["push", "press", "fly"], 3, 10),
    ("mantenimiento", "Mantenimiento de espalda", "Espalda", ["row", "remo", "pull"], 3, 10),
    ("mantenimiento", "Mantenimiento de piernas", "Piernas", ["squat", "sentadilla", "lunge"], 3, 10),
]


class Command(BaseCommand):
    help = "Crea o actualiza rutinas prehechas recomendadas por objetivo."

    @transaction.atomic
    def handle(self, *args, **options):
        catalog = Ejercicio.objects.filter(activo=True, propietario=None)
        PlantillaRutina.objects.filter(activa=True).update(activa=False)
        for objetivo, nombre, group_name, terms, series, reps in TEMPLATES:
            group, _ = GrupoMuscular.objects.get_or_create(
                nombre=group_name,
                defaults={"slug": slugify(group_name)},
            )
            plantilla, _ = PlantillaRutina.objects.update_or_create(
                objetivo=objetivo, nombre=nombre,
                defaults={
                    "descripcion": f"Rutina prehecha para trabajar {group_name.lower()} y avanzar hacia tu objetivo.",
                    "grupo_muscular": group,
                    "activa": True,
                },
            )
            plantilla.ejercicios.all().delete()
            usados = set()
            for term in terms:
                ejercicio = catalog.filter(
                    Q(nombre__icontains=term)
                    | Q(nombre_original__icontains=term)
                    | Q(grupo_muscular=group)
                ).exclude(pk__in=usados).first()
                if not ejercicio:
                    continue
                EjercicioDePlantilla.objects.create(
                    plantilla=plantilla, ejercicio=ejercicio, orden=len(usados) + 1,
                    series_objetivo=series, repeticiones_objetivo=reps,
                )
                usados.add(ejercicio.pk)
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(TEMPLATES)} plantillas creadas o actualizadas."
            )
        )
