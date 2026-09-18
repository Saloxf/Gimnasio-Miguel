from django.contrib import admin
from .models import SesionEntrenamiento, SerieEntrenamiento, Actividad, SegmentoKilometro
admin.site.register([SesionEntrenamiento, SerieEntrenamiento, Actividad, SegmentoKilometro])
