from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import RutinaForm, EjercicioDeRutinaForm
from ejercicios.models import GrupoMuscular
from .models import Rutina, EjercicioDeRutina, PlantillaRutina
class RutinaListView(LoginRequiredMixin, ListView):
    template_name = "rutinas/lista.html"; context_object_name = "rutinas"
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser) and not getattr(getattr(request.user, "perfil", None), "esta_completo", False):
            messages.info(request, "Completa tu perfil antes de crear o elegir una rutina.")
            return redirect("perfiles:perfil")
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self): return Rutina.objects.filter(usuario=self.request.user).prefetch_related("ejercicios_rutina__ejercicio")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objetivo = self.request.user.objetivos.filter(activo=True).first()
        plantillas = PlantillaRutina.objects.filter(activa=True)
        grupo_id = self.request.GET.get("grupo")
        if objetivo:
            recomendadas = plantillas.filter(objetivo=objetivo.tipo_objetivo)
            context["objetivo_activo"] = objetivo
        else:
            recomendadas = plantillas
        if grupo_id:
            recomendadas = recomendadas.filter(grupo_muscular_id=grupo_id)
        context["grupos_plantillas"] = GrupoMuscular.objects.filter(
            plantillas_rutina__activa=True
        ).distinct()
        context["grupo_seleccionado"] = grupo_id
        context["plantillas"] = recomendadas.select_related(
            "grupo_muscular"
        ).prefetch_related("ejercicios__ejercicio")
        return context
class RutinaCreateView(LoginRequiredMixin, CreateView):
    template_name = "rutinas/form.html"; form_class = RutinaForm; success_url = "/rutinas/"
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser) and not getattr(getattr(request.user, "perfil", None), "esta_completo", False):
            messages.info(request, "Completa tu perfil antes de crear una rutina.")
            return redirect("perfiles:perfil")
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form): form.instance.usuario = self.request.user; return super().form_valid(form)
class RutinaUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "rutinas/form.html"; form_class = RutinaForm; success_url = "/rutinas/"
    def get_queryset(self): return Rutina.objects.filter(usuario=self.request.user)
class RutinaDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "perfiles/confirmar_borrado.html"; success_url = "/rutinas/"
    def get_queryset(self): return Rutina.objects.filter(usuario=self.request.user)
class RutinaDetailView(LoginRequiredMixin, DetailView):
    template_name = "rutinas/detalle.html"; context_object_name = "rutina"
    def get_queryset(self): return Rutina.objects.filter(usuario=self.request.user).prefetch_related("ejercicios_rutina__ejercicio")
class EjercicioRutinaCreateView(LoginRequiredMixin, CreateView):
    template_name = "rutinas/ejercicio_form.html"; form_class = EjercicioDeRutinaForm
    def dispatch(self, request, *args, **kwargs): self.rutina = get_object_or_404(Rutina, pk=kwargs["rutina_id"], usuario=request.user); return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form): form.instance.rutina = self.rutina; return super().form_valid(form)
    def get_success_url(self): return f"/rutinas/{self.rutina.pk}/"
class EjercicioRutinaDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "perfiles/confirmar_borrado.html"
    def get_queryset(self): return EjercicioDeRutina.objects.filter(rutina__usuario=self.request.user)
    def get_success_url(self): return f"/rutinas/{self.object.rutina_id}/"
def duplicar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk, usuario=request.user); nueva = Rutina.objects.create(usuario=request.user, nombre=f"{rutina.nombre} (copia)", descripcion=rutina.descripcion)
    for item in rutina.ejercicios_rutina.all(): item.pk = None; item.rutina = nueva; item.save()
    messages.success(request, "Rutina duplicada."); return redirect("rutinas:detalle", pk=nueva.pk)

def usar_plantilla(request, pk):
    if not (request.user.is_staff or request.user.is_superuser) and not getattr(getattr(request.user, "perfil", None), "esta_completo", False):
        messages.info(request, "Completa tu perfil antes de elegir una rutina.")
        return redirect("perfiles:perfil")
    plantilla = get_object_or_404(
        PlantillaRutina.objects.prefetch_related("ejercicios__ejercicio"),
        pk=pk,
        activa=True,
    )
    rutina = Rutina.objects.create(
        usuario=request.user,
        nombre=plantilla.nombre,
        descripcion=plantilla.descripcion,
    )
    for item in plantilla.ejercicios.all():
        EjercicioDeRutina.objects.create(
            rutina=rutina,
            ejercicio=item.ejercicio,
            orden=item.orden,
            series_objetivo=item.series_objetivo,
            repeticiones_objetivo=item.repeticiones_objetivo,
            descanso_segundos=item.descanso_segundos,
        )
    messages.success(request, f"Rutina '{rutina.nombre}' creada desde una plantilla.")
    return redirect("rutinas:detalle", pk=rutina.pk)
