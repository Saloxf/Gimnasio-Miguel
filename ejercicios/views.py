from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db import models
from django.views.generic import DetailView, ListView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import EjercicioPropioForm
from .models import Ejercicio, GrupoMuscular


class EjercicioDetailView(LoginRequiredMixin, DetailView):
    model = Ejercicio
    template_name = "ejercicios/detalle.html"
    context_object_name = "ejercicio"

    def get_queryset(self):
        return Ejercicio.objects.filter(activo=True).filter(
            models.Q(propietario__isnull=True) | models.Q(propietario=self.request.user)
        ).select_related("grupo_muscular")


class BibliotecaView(LoginRequiredMixin, ListView):
    template_name = "ejercicios/biblioteca.html"; context_object_name = "ejercicios"; paginate_by = 20
    def get_queryset(self):
        qs = Ejercicio.objects.filter(activo=True).filter(
            models.Q(propietario__isnull=True) | models.Q(propietario=self.request.user)
        ).select_related("grupo_muscular")
        if self.request.GET.get("tipo"): qs = qs.filter(tipo_ejercicio=self.request.GET["tipo"])
        if self.request.GET.get("grupo"): qs = qs.filter(grupo_muscular_id=self.request.GET["grupo"])
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); ctx["grupos"] = GrupoMuscular.objects.all(); return ctx

class EjercicioPropioCreateView(LoginRequiredMixin, CreateView):
    template_name = "ejercicios/form.html"
    form_class = EjercicioPropioForm
    success_url = reverse_lazy("ejercicios:biblioteca")
    def form_valid(self, form):
        form.instance.propietario = self.request.user
        messages.success(self.request, "Ejercicio personalizado creado.")
        return super().form_valid(form)
