from django.db import models
class ConfiguracionGeneral(models.Model):
    TIPOS = [("texto", "Texto"), ("entero", "Entero"), ("decimal", "Decimal"), ("booleano", "Booleano")]
    clave = models.CharField(max_length=80, unique=True)
    valor = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TIPOS, default="texto")
    obligatorio = models.BooleanField(default=False)
    def __str__(self): return self.clave
class Contenido(models.Model):
    titulo = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    cuerpo = models.TextField()
    publicado = models.BooleanField(default=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    def __str__(self): return self.titulo
