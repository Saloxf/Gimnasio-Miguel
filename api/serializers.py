from rest_framework import serializers
from rutinas.models import Rutina, EjercicioDeRutina
from entrenamientos.models import SesionEntrenamiento, SerieEntrenamiento, Actividad
class RutinaSerializer(serializers.ModelSerializer):
    volumen = serializers.SerializerMethodField()
    class Meta: model = Rutina; fields = ["id", "nombre", "descripcion", "activa", "volumen", "creado_en"]
    def get_volumen(self, obj): return obj.volumen_objetivo()
class SerieSerializer(serializers.ModelSerializer):
    volumen = serializers.ReadOnlyField()
    class Meta: model = SerieEntrenamiento; fields = ["id", "ejercicio", "numero_serie", "peso", "repeticiones", "volumen", "completado_en"]

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ["id", "nombre", "tipo", "realizada_en", "duracion_minutos", "distancia_km", "calorias", "notas"]
