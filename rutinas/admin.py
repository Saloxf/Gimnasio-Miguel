from django.contrib import admin
from .models import Rutina, EjercicioDeRutina
admin.site.register([Rutina, EjercicioDeRutina])
from django.contrib import admin
from .models import PlantillaRutina, EjercicioDePlantilla

admin.site.register([PlantillaRutina, EjercicioDePlantilla])
