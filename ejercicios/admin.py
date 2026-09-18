from django.contrib import admin
from .models import GrupoMuscular, Ejercicio
@admin.register(GrupoMuscular)
class GrupoAdmin(admin.ModelAdmin): prepopulated_fields = {"slug": ("nombre",)}; search_fields = ("nombre",)
@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "grupo_muscular", "tipo_ejercicio", "propietario", "activo")
    list_filter = ("tipo_ejercicio", "activo", "grupo_muscular"); search_fields = ("nombre",)
