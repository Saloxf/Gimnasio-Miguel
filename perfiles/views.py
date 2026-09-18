from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView
from .forms import PerfilForm, ObjetivoForm, RegistroPesoForm
from .models import Perfil, Objetivo, RegistroPeso
class PerfilView(LoginRequiredMixin, UpdateView):
    template_name = "perfiles/perfil_form.html"; form_class = PerfilForm; success_url = "/perfil/"
    def get_object(self, queryset=None): return Perfil.objects.get_or_create(usuario=self.request.user)[0]
    def form_valid(self, form):
        form.instance.usuario = self.request.user; messages.success(self.request, "Perfil actualizado."); return super().form_valid(form)
class ObjetivoListView(LoginRequiredMixin, ListView):
    template_name = "perfiles/objetivos.html"; context_object_name = "objetivos"
    def get_queryset(self): return Objetivo.objects.filter(usuario=self.request.user)
class ObjetivoCreateView(LoginRequiredMixin, CreateView):
    template_name = "perfiles/objetivo_form.html"; form_class = ObjetivoForm; success_url = "/perfil/objetivos/"
    def form_valid(self, form): form.instance.usuario = self.request.user; return super().form_valid(form)
class ObjetivoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "perfiles/objetivo_form.html"; form_class = ObjetivoForm; success_url = "/perfil/objetivos/"
    def get_queryset(self): return Objetivo.objects.filter(usuario=self.request.user)
class ObjetivoDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "perfiles/confirmar_borrado.html"; success_url = "/perfil/objetivos/"
    def get_queryset(self): return Objetivo.objects.filter(usuario=self.request.user)

class RegistroPesoView(LoginRequiredMixin, FormView):
    template_name = "perfiles/peso.html"
    form_class = RegistroPesoForm
    success_url = "/perfil/peso/"
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.save()
        messages.success(self.request, "Peso registrado correctamente.")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["registros"] = RegistroPeso.objects.filter(usuario=self.request.user)[:30]
        return context
