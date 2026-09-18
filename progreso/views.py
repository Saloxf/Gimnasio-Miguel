from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Sum, F, DecimalField, ExpressionWrapper
from django.http import JsonResponse
from django.views.generic import TemplateView
from entrenamientos.models import SesionEntrenamiento, SerieEntrenamiento
from .models import RecordPersonal
class ProgresoView(LoginRequiredMixin, TemplateView):
    template_name = "progreso/inicio.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); series = SerieEntrenamiento.objects.filter(sesion__usuario=self.request.user)
        ctx["volumen_total"] = sum((s.peso * s.repeticiones for s in series), 0)
        ctx["records"] = RecordPersonal.objects.filter(usuario=self.request.user).select_related("ejercicio")[:10]
        ctx["entrenamientos"] = SesionEntrenamiento.objects.filter(usuario=self.request.user).count()
        return ctx
