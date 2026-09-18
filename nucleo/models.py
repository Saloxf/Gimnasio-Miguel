from django.db import models
class RedSocial(models.Model):
    nombre = models.CharField(max_length=40)
    url = models.URLField()
    icono = models.CharField(max_length=40, default="link")
    activa = models.BooleanField(default=True)
    class Meta: ordering = ["nombre"]
    def __str__(self): return self.nombre
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    mensaje = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)
    class Meta: ordering = ["-creado_en"]
