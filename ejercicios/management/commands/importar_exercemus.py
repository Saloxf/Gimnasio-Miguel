import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ejercicios.models import Ejercicio, GrupoMuscular


GROUP_NAMES = {
    "arms": "Brazos",
    "back": "Espalda",
    "calves": "Pantorrillas",
    "chest": "Pecho",
    "core": "Core",
    "legs": "Piernas",
    "shoulders": "Hombros",
}

NAME_TRANSLATIONS = {
    "ab roller": "rueda abdominal",
    "adductor": "aductor",
    "advanced": "avanzado",
    "air bike": "bicicleta de aire",
    "all fours": "en cuatro apoyos",
    "alternate": "alterno",
    "alternating": "alternado",
    "ankle": "tobillo",
    "anti-gravity": "antigravedad",
    "anterior tibialis": "tibial anterior",
    "arm circles": "círculos de brazos",
    "around the worlds": "vueltas al mundo",
    "atlas stone": "piedra atlas",
    "ab wheel": "rueda abdominal",
    "back extension": "extensión de espalda",
    "backward": "hacia atrás",
    "balance board": "tabla de equilibrio",
    "ball": "balón",
    "band": "banda",
    "bench press": "press de banca",
    "bent over": "inclinado",
    "biceps": "bíceps",
    "cable": "polea",
    "calf": "pantorrilla",
    "chest": "pecho",
    "chin-up": "dominada supina",
    "crunch": "abdominal",
    "clean": "cargada",
    "curl": "curl",
    "deadlift": "peso muerto",
    "dips": "fondos",
    "dumbbell": "mancuerna",
    "floor": "suelo",
    "fly": "apertura",
    "front raise": "elevación frontal",
    "good morning": "buenos días",
    "glute": "glúteo",
    "hamstring": "femoral",
    "hammer": "martillo",
    "heel": "talón",
    "hip": "cadera",
    "jump": "salto",
    "incline": "inclinado",
    "kettlebell": "pesa rusa",
    "leg": "pierna",
    "lateral raise": "elevación lateral",
    "lunge": "zancada",
    "machine": "máquina",
    "military press": "press militar",
    "medicine ball": "balón medicinal",
    "overhead": "sobre la cabeza",
    "plank": "plancha",
    "press": "press",
    "pull-up": "dominada",
    "push-up": "flexión",
    "quad": "cuádriceps",
    "reverse": "invertido",
    "rowing": "remo",
    "row": "remo",
    "renegade": "renegado",
    "shoulder": "hombro",
    "shrug": "encogimiento",
    "sit-up": "abdominal completo",
    "squat": "sentadilla",
    "standing": "de pie",
    "stretch": "estiramiento",
    "triceps": "tríceps",
    "touchers": "toques",
    "upright": "vertical",
    "wrist": "muñeca",
}


def translate_name(name):
    translated = name
    for source, target in sorted(NAME_TRANSLATIONS.items(), key=lambda item: -len(item[0])):
        translated = re.sub(rf"\b{re.escape(source)}\b", target, translated, flags=re.IGNORECASE)
    return translated


def exercise_type(category):
    return {
        "cardio": "cardio",
        "stretching": "movilidad",
        "calisthenics": "calistenia",
    }.get(category, "fuerza")


class Command(BaseCommand):
    help = "Importa el catálogo abierto de 872 ejercicios de exercemus."

    def add_arguments(self, parser):
        parser.add_argument(
            "--archivo",
            type=Path,
            default=Path(__file__).resolve().parents[2] / "data" / "exercemus_exercises.json",
        )

    def handle(self, *args, **options):
        path = options["archivo"]
        if not path.is_file():
            raise self.CommandError(f"No existe el archivo de ejercicios: {path}")

        with path.open(encoding="utf-8") as source:
            catalog = json.load(source)

        muscle_groups = catalog.get("muscle_groups", {})
        muscle_to_group = {
            muscle: group for group, muscles in muscle_groups.items() for muscle in muscles
        }
        imported = 0
        updated = 0

        for item in catalog.get("exercises", []):
            primary_muscles = item.get("primary_muscles") or []
            group_key = muscle_to_group.get(primary_muscles[0], "general")
            group_name = GROUP_NAMES.get(group_key, "General")
            group, _ = GrupoMuscular.objects.get_or_create(
                nombre=group_name,
                defaults={"slug": slugify(group_name)},
            )
            license_data = item.get("license") or {}
            defaults = {
                "nombre": translate_name(item["name"]),
                "nombre_original": item["name"],
                "tipo_ejercicio": exercise_type(item.get("category", "")),
                "descripcion": item.get("description") or "",
                "instrucciones": "\n".join(
                    f"{index}. {instruction}"
                    for index, instruction in enumerate(item.get("instructions") or [], 1)
                ),
                "equipamiento": ", ".join(item.get("equipment") or []),
                "categoria_fuente": item.get("category") or "",
                "alias": item.get("aliases") or [],
                "musculos_principales": primary_muscles,
                "musculos_secundarios": item.get("secondary_muscles") or [],
                "consejos": item.get("tips") or [],
                "tempo": item.get("tempo") or "",
                "video_url": item.get("video") or "",
                "fuente": "exercemus",
                "autor_fuente": item.get("license_author") or "",
                "licencia_nombre": license_data.get("full_name") or "",
                "licencia_url": license_data.get("url") or "",
                "activo": True,
            }
            exercise = Ejercicio.objects.filter(
                grupo_muscular=group, propietario=None
            ).filter(
                nombre_original=item["name"]
            ).first() or Ejercicio.objects.filter(
                nombre=item["name"], grupo_muscular=group, propietario=None
            ).first()
            created = exercise is None
            if created:
                exercise = Ejercicio.objects.create(
                    grupo_muscular=group, propietario=None, **defaults
                )
            else:
                for field, value in defaults.items():
                    setattr(exercise, field, value)
                exercise.save(update_fields=list(defaults) + ["grupo_muscular"])
            imported += created
            updated += not created

        self.stdout.write(
            self.style.SUCCESS(
                f"Catálogo exercemus cargado: {imported} creados, {updated} actualizados."
            )
        )
