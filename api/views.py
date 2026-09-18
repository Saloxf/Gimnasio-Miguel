from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from perfiles.models import RegistroPeso
from ejercicios.models import Ejercicio, GrupoMuscular
from rutinas.models import Rutina
from entrenamientos.models import SesionEntrenamiento, SerieEntrenamiento, Actividad
from .serializers import RutinaSerializer, SerieSerializer, ActividadSerializer
class RutinaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RutinaSerializer
    def get_queryset(self): return Rutina.objects.filter(usuario=self.request.user)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def resumen_progreso(request):
    series = SerieEntrenamiento.objects.filter(sesion__usuario=request.user).select_related("ejercicio")
    datos = [{"fecha": s.completado_en.date(), "ejercicio": s.ejercicio.nombre, "volumen": float(s.peso*s.repeticiones)} for s in series[:100]]
    return Response({"datos": datos})
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def registrar_serie_api(request):
    sesion = SesionEntrenamiento.objects.filter(pk=request.data.get("sesion"), usuario=request.user).first()
    if not sesion: return Response({"detalle": "Sesión no encontrada."}, status=404)
    serializer = SerieSerializer(data=request.data)
    if serializer.is_valid():
        serie = serializer.save(sesion=sesion); return Response(SerieSerializer(serie).data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def peso_api(request):
    if request.method == "POST":
        registro = RegistroPeso.objects.create(usuario=request.user, peso_kg=request.data.get("peso_kg"), notas=request.data.get("notas", ""))
        return Response({"id": registro.id, "peso_kg": registro.peso_kg, "registrado_en": registro.registrado_en}, status=201)
    registros = RegistroPeso.objects.filter(usuario=request.user).values("peso_kg", "registrado_en")
    return Response(list(registros))

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def exportar_plan(request):
    rutinas = Rutina.objects.filter(usuario=request.user).prefetch_related("ejercicios_rutina__ejercicio")
    data = {"version": 1, "rutinas": []}
    for rutina in rutinas:
        data["rutinas"].append({
            "nombre": rutina.nombre,
            "descripcion": rutina.descripcion,
            "activa": rutina.activa,
            "ejercicios": [{
                "nombre": item.ejercicio.nombre, "grupo": item.ejercicio.grupo_muscular.nombre,
                "tipo": item.ejercicio.tipo_ejercicio, "orden": item.orden,
                "series": item.series_objetivo, "repeticiones": item.repeticiones_objetivo,
                "peso": str(item.peso_objetivo), "descanso": item.descanso_segundos,
            } for item in rutina.ejercicios_rutina.all()],
        })
    response = JsonResponse(data)
    response["Content-Disposition"] = 'attachment; filename="fittrack-plan.json"'
    return response

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def importar_plan(request):
    payload = request.data
    if not isinstance(payload, dict) or not isinstance(payload.get("rutinas"), list):
        return Response({"detalle": "El archivo no tiene un formato de plan válido."}, status=400)
    creadas = 0
    with transaction.atomic():
        for item in payload["rutinas"]:
            rutina = Rutina.objects.create(usuario=request.user, nombre=item.get("nombre", "Rutina importada"), descripcion=item.get("descripcion", ""), activa=item.get("activa", True))
            for exercise in item.get("ejercicios", []):
                grupo, _ = GrupoMuscular.objects.get_or_create(nombre=exercise.get("grupo", "General"), defaults={"slug": f"general-{request.user.pk}"})
                ejercicio, _ = Ejercicio.objects.get_or_create(nombre=exercise.get("nombre", "Ejercicio importado"), grupo_muscular=grupo, propietario=request.user, defaults={"tipo_ejercicio": exercise.get("tipo", "fuerza")})
                from rutinas.models import EjercicioDeRutina
                EjercicioDeRutina.objects.create(rutina=rutina, ejercicio=ejercicio, orden=exercise.get("orden", 1), series_objetivo=exercise.get("series", 3), repeticiones_objetivo=exercise.get("repeticiones", 10), peso_objetivo=exercise.get("peso", 0), descanso_segundos=exercise.get("descanso", 90))
            creadas += 1
    return Response({"rutinas_creadas": creadas}, status=201)

@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def actividades_api(request):
    if request.method == "GET":
        queryset = Actividad.objects.filter(usuario=request.user)
        return Response(ActividadSerializer(queryset, many=True).data)
    serializer = ActividadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    actividad = serializer.save(usuario=request.user)
    return Response(ActividadSerializer(actividad).data, status=201)
