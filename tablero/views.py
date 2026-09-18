from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView
from rutinas.models import Rutina
from entrenamientos.models import SesionEntrenamiento, SerieEntrenamiento
from progreso.models import RecordPersonal
class TableroView(LoginRequiredMixin, TemplateView):
    template_name = "tablero/inicio.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return redirect(reverse("paneladmin:inicio"))
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); ahora = timezone.now(); inicio = ahora - timedelta(days=7)
        sesiones = SesionEntrenamiento.objects.filter(usuario=self.request.user)
        ctx.update({"rutinas": Rutina.objects.filter(usuario=self.request.user), "ultima_sesion": sesiones.first(), "sesiones_semana": sesiones.filter(iniciado_en__gte=inicio).count(), "records": RecordPersonal.objects.filter(usuario=self.request.user).select_related("ejercicio")[:4], "volumen_semanal": sum((s.peso*s.repeticiones for s in SerieEntrenamiento.objects.filter(sesion__usuario=self.request.user, completado_en__gte=inicio)), 0)})
        return ctx
