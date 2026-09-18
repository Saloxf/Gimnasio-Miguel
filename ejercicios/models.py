from django.conf import settings
from django.db import models
from django.templatetags.static import static
from urllib.parse import parse_qs, urlparse

class GrupoMuscular(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    descripcion = models.TextField(blank=True)
    class Meta: ordering = ["nombre"]
    def __str__(self): return self.nombre

class Ejercicio(models.Model):
    TIPOS = [("fuerza", "Fuerza"), ("cardio", "Cardio"), ("movilidad", "Movilidad"), ("calistenia", "Calistenia")]
    nombre = models.CharField(max_length=120)
    nombre_original = models.CharField(max_length=120, blank=True)
    grupo_muscular = models.ForeignKey(GrupoMuscular, on_delete=models.PROTECT, related_name="ejercicios")
    tipo_ejercicio = models.CharField(max_length=20, choices=TIPOS, default="fuerza")
    descripcion = models.TextField(blank=True)
    instrucciones = models.TextField(blank=True)
    equipamiento = models.CharField(max_length=120, blank=True)
    categoria_fuente = models.CharField(max_length=80, blank=True)
    alias = models.JSONField(default=list, blank=True)
    musculos_principales = models.JSONField(default=list, blank=True)
    musculos_secundarios = models.JSONField(default=list, blank=True)
    consejos = models.JSONField(default=list, blank=True)
    tempo = models.CharField(max_length=30, blank=True)
    video_url = models.URLField(blank=True)
    fuente = models.CharField(max_length=80, blank=True)
    autor_fuente = models.CharField(max_length=160, blank=True)
    licencia_nombre = models.CharField(max_length=160, blank=True)
    licencia_url = models.URLField(blank=True)
    dataset_id = models.CharField(max_length=20, blank=True, db_index=True)
    parte_cuerpo = models.CharField(max_length=80, blank=True)
    objetivo = models.CharField(max_length=80, blank=True)
    imagen_url = models.URLField(blank=True)
    gif_url = models.URLField(blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="ejercicios_creados")
    propietario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="ejercicios_propios")
    activo = models.BooleanField(default=True)
    class Meta:
        ordering = ["grupo_muscular__nombre", "nombre"]
        constraints = [
            models.UniqueConstraint(fields=["nombre", "grupo_muscular"], condition=models.Q(propietario__isnull=True), name="ejercicio_catalogo_nombre_grupo_unico"),
            models.UniqueConstraint(fields=["nombre", "grupo_muscular", "propietario"], name="ejercicio_usuario_nombre_grupo_unico"),
        ]
    def __str__(self): return self.nombre

    @property
    def media_url(self):
        return self.gif_url or self.imagen_url or static("img/exercise-placeholder.svg")

    @property
    def video_embed_url(self):
        if not self.video_url:
            return ""
        parsed = urlparse(self.video_url)
        video_id = parse_qs(parsed.query).get("v", [None])[0]
        if parsed.hostname in {"youtu.be", "www.youtu.be"}:
            video_id = parsed.path.strip("/")
        if parsed.hostname in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
            if parsed.path.startswith("/embed/"):
                video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
        return f"https://www.youtube.com/embed/{video_id}" if video_id else ""
