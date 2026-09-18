from django.conf import settings
from django.db import models
from ejercicios.models import Ejercicio

class RecordPersonal(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="records")
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, related_name="records")
    peso = models.DecimalField(max_digits=7, decimal_places=2)
    repeticiones = models.PositiveIntegerField()
    logrado_en = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-peso", "-logrado_en"]
        constraints = [models.UniqueConstraint(fields=["usuario", "ejercicio", "peso", "repeticiones"], name="record_unico")]
