from django.conf import settings
from django.db import models
from rutinas.models import Rutina
from ejercicios.models import Ejercicio

class SesionEntrenamiento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sesiones")
    rutina = models.ForeignKey(Rutina, null=True, blank=True, on_delete=models.SET_NULL, related_name="sesiones")
    iniciado_en = models.DateTimeField(auto_now_add=True)
    finalizado_en = models.DateTimeField(null=True, blank=True)
    notas = models.TextField(blank=True)
    class Meta: ordering = ["-iniciado_en"]
    def volumen_total(self):
        return sum((serie.peso * serie.repeticiones for serie in self.series.all()), 0)
    def __str__(self): return f"Sesión {self.iniciado_en:%d/%m/%Y}"

class SerieEntrenamiento(models.Model):
    sesion = models.ForeignKey(SesionEntrenamiento, on_delete=models.CASCADE, related_name="series")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.PROTECT, related_name="series_registradas")
    numero_serie = models.PositiveIntegerField()
    peso = models.DecimalField(max_digits=7, decimal_places=2)
    repeticiones = models.PositiveIntegerField()
    descanso_segundos = models.PositiveIntegerField(default=0)
    completado_en = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["ejercicio", "numero_serie"]
        constraints = [models.UniqueConstraint(fields=["sesion", "ejercicio", "numero_serie"], name="serie_numero_unico")]
    @property
    def volumen(self): return self.peso * self.repeticiones

class Actividad(models.Model):
    TIPOS = [
        ("correr", "Correr"), ("ciclismo", "Ciclismo"), ("natacion", "Natación"),
        ("caminar", "Caminar"), ("otro", "Otro"),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actividades")
    nombre = models.CharField(max_length=140)
    tipo = models.CharField(max_length=20, choices=TIPOS, default="otro")
    realizada_en = models.DateTimeField()
    duracion_minutos = models.PositiveIntegerField(default=0)
    distancia_km = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    calorias = models.PositiveIntegerField(null=True, blank=True)
    notas = models.TextField(blank=True)
    archivo_gpx = models.FileField(upload_to="gpx/%Y/%m/", blank=True)
    datos_ruta = models.JSONField(default=list, blank=True)
    datos_elevacion = models.JSONField(default=list, blank=True)
    distancia_metros = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    elevacion_ganada_m = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    elevacion_perdida_m = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-realizada_en"]
    def __str__(self):
        return f"{self.nombre} · {self.realizada_en:%d/%m/%Y}"

class SegmentoKilometro(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="segmentos")
    numero = models.PositiveIntegerField()
    distancia_metros = models.DecimalField(max_digits=8, decimal_places=2)
    duracion_segundos = models.PositiveIntegerField()
    ritmo_segundos_km = models.PositiveIntegerField(null=True, blank=True)
    elevacion_ganada_m = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    elevacion_perdida_m = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    class Meta:
        ordering = ["numero"]
        constraints = [models.UniqueConstraint(fields=["actividad", "numero"], name="segmento_km_unico")]
