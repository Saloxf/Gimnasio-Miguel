from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Max
from django.db import IntegrityError, transaction
from rutinas.models import Rutina
from ejercicios.models import Ejercicio
from .forms import SerieForm, ActividadForm
from .models import SesionEntrenamiento, SerieEntrenamiento, Actividad, SegmentoKilometro
from .gpx import analizar_gpx
class HistorialView(LoginRequiredMixin, ListView):
    template_name = "entrenamientos/historial.html"; context_object_name = "sesiones"
    def get_queryset(self): return SesionEntrenamiento.objects.filter(usuario=self.request.user).select_related("rutina").prefetch_related("series__ejercicio")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actividades"] = Actividad.objects.filter(usuario=self.request.user)
        return context

class ActividadCreateView(LoginRequiredMixin, CreateView):
    template_name = "entrenamientos/actividad_form.html"
    form_class = ActividadForm
    success_url = "/entrenamientos/"
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        if form.cleaned_data.get("archivo_gpx"):
            try:
                datos = analizar_gpx(form.cleaned_data["archivo_gpx"])
            except (ValueError, OSError) as error:
                form.add_error("archivo_gpx", str(error))
                return self.form_invalid(form)
            form.instance.datos_ruta = datos["ruta"]
            form.instance.datos_elevacion = datos["elevacion"]
            form.instance.distancia_metros = datos["distancia_metros"]
            form.instance.distancia_km = datos["distancia_metros"] / 1000
            form.instance.duracion_minutos = max(1, round(datos["duracion_segundos"] / 60))
            form.instance.elevacion_ganada_m = datos["elevacion_ganada"]
            form.instance.elevacion_perdida_m = datos["elevacion_perdida"]
            self.segmentos = datos["segmentos"]
        messages.success(self.request, "Actividad guardada correctamente.")
        response = super().form_valid(form)
        for segmento in getattr(self, "segmentos", []):
            SegmentoKilometro.objects.create(actividad=self.object, **segmento)
        return response
    def get_success_url(self):
        return f"/entrenamientos/actividad/{self.object.pk}/"

class ActividadDetailView(LoginRequiredMixin, DetailView):
    template_name = "entrenamientos/actividad.html"
    context_object_name = "actividad"
    def get_queryset(self):
        return Actividad.objects.filter(usuario=self.request.user).prefetch_related("segmentos")
class SesionDetailView(LoginRequiredMixin, DetailView):
    template_name = "entrenamientos/sesion.html"; context_object_name = "sesion"
    def get_queryset(self): return SesionEntrenamiento.objects.filter(usuario=self.request.user).prefetch_related("series__ejercicio")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SerieForm()
        if self.object.rutina:
            context["form"].fields["ejercicio"].queryset = Ejercicio.objects.filter(usos_en_rutinas__rutina=self.object.rutina)
        return context
def iniciar_entrenamiento(request, rutina_id=None):
    if not (request.user.is_staff or request.user.is_superuser) and not getattr(getattr(request.user, "perfil", None), "esta_completo", False):
        messages.info(request, "Completa tu perfil antes de comenzar un entrenamiento.")
        return redirect("perfiles:perfil")
    rutina = get_object_or_404(Rutina, pk=rutina_id, usuario=request.user) if rutina_id else None
    sesion = SesionEntrenamiento.objects.create(usuario=request.user, rutina=rutina)
    return redirect("entrenamientos:sesion", pk=sesion.pk)
def registrar_serie(request, sesion_id):
    sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id, usuario=request.user)
    if request.method != "POST":
        return redirect("entrenamientos:sesion", pk=sesion.pk)

    form = SerieForm(request.POST)
    if not form.is_valid():
        return render(request, "entrenamientos/sesion.html", {"sesion": sesion, "form": form})

    serie = form.save(commit=False)
    serie.sesion = sesion
    if sesion.finalizado_en:
        form.add_error(None, "Este entrenamiento ya fue finalizado y no acepta nuevas series.")
    elif sesion.rutina and not sesion.rutina.ejercicios_rutina.filter(
        ejercicio=serie.ejercicio
    ).exists():
        form.add_error("ejercicio", "El ejercicio no pertenece a esta rutina.")
    elif SerieEntrenamiento.objects.filter(
        sesion=sesion,
        ejercicio=serie.ejercicio,
        numero_serie=serie.numero_serie,
    ).exists():
        form.add_error(
            "numero_serie",
            "Esta serie ya está registrada. Usa otro número o revisa las series guardadas.",
        )

    if form.errors:
        return render(request, "entrenamientos/sesion.html", {"sesion": sesion, "form": form})

    try:
        with transaction.atomic():
            serie.save()
    except IntegrityError:
        form.add_error(
            "numero_serie",
            "Esta serie ya fue registrada. Actualiza la página y usa el siguiente número.",
        )
        return render(request, "entrenamientos/sesion.html", {"sesion": sesion, "form": form})

    mejor = SerieEntrenamiento.objects.filter(
        sesion__usuario=request.user, ejercicio=serie.ejercicio
    ).order_by("-peso", "-repeticiones").first()
    if mejor:
        from progreso.models import RecordPersonal
        RecordPersonal.objects.get_or_create(
            usuario=request.user, ejercicio=serie.ejercicio,
            peso=mejor.peso, repeticiones=mejor.repeticiones,
        )
    messages.success(request, "Serie registrada.")
    return redirect("entrenamientos:sesion", pk=sesion.pk)
def finalizar_entrenamiento(request, pk):
    sesion = get_object_or_404(SesionEntrenamiento, pk=pk, usuario=request.user)
    if not sesion.series.exists():
        messages.error(request, "Registra al menos un ejercicio antes de finalizar la sesión.")
        return redirect("entrenamientos:sesion", pk=sesion.pk)
    sesion.finalizado_en = timezone.now()
    sesion.save(update_fields=["finalizado_en"])
    messages.success(request, "Entrenamiento finalizado.")
    return redirect("entrenamientos:historial")
