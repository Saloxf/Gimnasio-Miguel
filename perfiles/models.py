from django.conf import settings
from django.db import models

class Perfil(models.Model):
    SEXOS = [("femenino", "Femenino"), ("masculino", "Masculino"), ("otro", "Otro"), ("prefiero_no_decirlo", "Prefiero no decirlo")]
    NIVELES = [("principiante", "Principiante"), ("intermedio", "Intermedio"), ("avanzado", "Avanzado")]
    FRECUENCIAS = [(str(n), f"{n} días por semana") for n in range(1, 8)]
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=30, choices=SEXOS, blank=True)
    altura_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    nivel_experiencia = models.CharField(max_length=20, choices=NIVELES, blank=True)
    frecuencia_entrenamiento = models.CharField(max_length=1, choices=FRECUENCIAS, blank=True)
    @property
    def esta_completo(self):
        return all([
            self.edad,
            self.sexo,
            self.altura_cm,
            self.peso_kg,
            self.nivel_experiencia,
            self.frecuencia_entrenamiento,
        ])
    def imc(self):
        if self.peso_kg and self.altura_cm:
            return round(float(self.peso_kg) / (float(self.altura_cm) / 100) ** 2, 2)
        return None
    def __str__(self): return f"Perfil de {self.usuario}"

class Objetivo(models.Model):
    TIPOS = [("ganancia_muscular", "Ganancia muscular"), ("fuerza", "Fuerza"), ("perdida_grasa", "Pérdida de grasa"), ("condicion_fisica", "Condición física"), ("mantenimiento", "Mantenimiento")]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="objetivos")
    tipo_objetivo = models.CharField(max_length=30, choices=TIPOS)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-activo", "-creado_en"]
    def __str__(self): return self.get_tipo_objetivo_display()

class RegistroPeso(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="registros_peso")
    peso_kg = models.DecimalField(max_digits=6, decimal_places=2)
    registrado_en = models.DateTimeField(auto_now_add=True)
    notas = models.CharField(max_length=200, blank=True)
    class Meta:
        ordering = ["registrado_en"]
    def __str__(self):
        return f"{self.peso_kg} kg · {self.registrado_en:%d/%m/%Y}"
