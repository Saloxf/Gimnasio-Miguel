import json
from pathlib import Path
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ejercicios.models import Ejercicio, GrupoMuscular


DATASET_URL = (
    "https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/"
    "data/exercises.json"
)
MEDIA_BASE_URL = (
    "https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/"
)

GROUP_NAMES = {
    "back": "Espalda",
    "cardio": "Cardio",
    "chest": "Pecho",
    "lower arms": "Antebrazos",
    "lower legs": "Pantorrillas",
    "neck": "Cuello",
    "shoulders": "Hombros",
    "upper arms": "Brazos",
    "upper legs": "Piernas",
    "waist": "Core",
}


def exercise_type(category):
    if category == "cardio":
        return "cardio"
    if category in {"stretching", "flexibility"}:
        return "movilidad"
    if category in {"calisthenics", "plyometrics"}:
        return "calistenia"
    return "fuerza"


class Command(BaseCommand):
    help = "Importa ejercicios, miniaturas JPG y animaciones GIF del dataset abierto."

    def add_arguments(self, parser):
        parser.add_argument("--archivo", type=Path)
        parser.add_argument("--limit", type=int)

    def handle(self, *args, **options):
        source_path = options.get("archivo")
        if source_path:
            if not source_path.is_file():
                raise self.CommandError(f"No existe el archivo: {source_path}")
            with source_path.open(encoding="utf-8") as source:
                dataset = json.load(source)
        else:
            request = Request(DATASET_URL, headers={"User-Agent": "FitTrack importer"})
            try:
                with urlopen(request, timeout=60) as response:
                    dataset = json.load(response)
            except OSError as error:
                raise self.CommandError(
                    f"No se pudo descargar el dataset: {error}"
                ) from error

        imported = updated = 0
        records = dataset[: options["limit"]] if options.get("limit") else dataset
        for item in records:
            dataset_id = str(item["id"])
            body_part = item.get("body_part") or item.get("category") or "general"
            group_name = GROUP_NAMES.get(body_part.lower(), body_part.title())
            group, _ = GrupoMuscular.objects.get_or_create(
                nombre=group_name,
                defaults={"slug": slugify(group_name)},
            )
            instructions = item.get("instructions") or {}
            instruction_text = instructions.get("es") or instructions.get("en") or ""
            steps = item.get("instruction_steps") or {}
            if steps.get("es") or steps.get("en"):
                instruction_text = "\n".join(
                    f"{index}. {step}"
                    for index, step in enumerate(steps.get("es") or steps["en"], 1)
                )
            defaults = {
                "nombre": item["name"].strip().title(),
                "nombre_original": item["name"],
                "tipo_ejercicio": exercise_type(item.get("category", "")),
                "descripcion": f"Ejercicio para {item.get('target') or body_part}.",
                "instrucciones": instruction_text,
                "equipamiento": item.get("equipment") or "",
                "categoria_fuente": item.get("category") or "",
                "parte_cuerpo": body_part,
                "objetivo": item.get("target") or "",
                "dataset_id": dataset_id,
                "imagen_url": (
                    MEDIA_BASE_URL + item["image"] if item.get("image") else ""
                ),
                "gif_url": (
                    MEDIA_BASE_URL + item["gif_url"] if item.get("gif_url") else ""
                ),
                "fuente": "exercises-dataset",
                "autor_fuente": "Gym visual",
                "licencia_nombre": "MIT + media terms",
                "licencia_url": (
                    "https://github.com/hasaneyldrm/exercises-dataset/blob/main/LICENSE"
                ),
                "activo": True,
                "propietario": None,
            }
            exercise = Ejercicio.objects.filter(
                dataset_id=dataset_id, propietario=None
            ).first()
            if exercise is None:
                exercise = Ejercicio.objects.filter(
                    nombre=defaults["nombre"],
                    grupo_muscular=group,
                    propietario=None,
                ).first()
            created = exercise is None
            if created:
                exercise = Ejercicio.objects.create(
                    grupo_muscular=group, **defaults
                )
            else:
                for field, value in defaults.items():
                    setattr(exercise, field, value)
                exercise.grupo_muscular = group
                exercise.save()
            imported += created
            updated += not created

        self.stdout.write(
            self.style.SUCCESS(
                f"Dataset cargado: {imported} creados, {updated} actualizados."
            )
        )
