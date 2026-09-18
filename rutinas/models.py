from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from ejercicios.models import Ejercicio, GrupoMuscular

class PlantillaRutina(models.Model):
    OBJETIVOS = [
        ("ganancia_muscular", "Ganancia muscular"),
        ("fuerza", "Fuerza"),
        ("perdida_grasa", "Pérdida de grasa"),
        ("condicion_fisica", "Condición física"),
        ("mantenimiento", "Mantenimiento"),
    ]
    nombre = models.CharField(max_length=120)
    objetivo = models.CharField(max_length=30, choices=OBJETIVOS)
    descripcion = models.TextField(blank=True)
    nivel = models.CharField(max_length=20, default="principiante")
    dias_semana = models.PositiveSmallIntegerField(default=3)
    grupo_muscular = models.ForeignKey(
        GrupoMuscular,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="plantillas_rutina",
    )
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["objetivo", "nombre"]

    def __str__(self):
        return self.nombre

class Rutina(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rutinas")
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    class Meta: ordering = ["-creado_en"]
    def volumen_objetivo(self):
        return sum((item.volumen_objetivo() for item in self.ejercicios_rutina.all()), Decimal("0"))
    def __str__(self): return self.nombre

class EjercicioDeRutina(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name="ejercicios_rutina")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT, related_name="usos_en_rutinas")
    orden = models.PositiveIntegerField(default=1)
    series_objetivo = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1)])
    repeticiones_objetivo = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    peso_objetivo = models.DecimalField(max_digits=7, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    descanso_segundos = models.PositiveIntegerField(default=90)
    class Meta:
        ordering = ["orden"]
        constraints = [models.UniqueConstraint(fields=["rutina", "ejercicio"], name="ejercicio_unico_por_rutina")]
    def volumen_objetivo(self): return self.series_objetivo * self.repeticiones_objetivo * self.peso_objetivo

class EjercicioDePlantilla(models.Model):
    plantilla = models.ForeignKey(PlantillaRutina, on_delete=models.CASCADE, related_name="ejercicios")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT)
    orden = models.PositiveIntegerField(default=1)
    series_objetivo = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1)])
    repeticiones_objetivo = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    descanso_segundos = models.PositiveIntegerField(default=90)

    class Meta:
        ordering = ["orden"]
        constraints = [
            models.UniqueConstraint(
                fields=["plantilla", "ejercicio"],
                name="ejercicio_unico_por_plantilla",
            )
        ]
