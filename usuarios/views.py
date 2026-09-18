from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroForm, LoginForm
class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "usuarios/registro.html"
    success_url = reverse_lazy("tablero:inicio")
    def form_valid(self, form):
        response = super().form_valid(form); login(self.request, self.object); messages.success(self.request, "¡Bienvenido a CundiFit!"); return response
class LoginUsuarioView(LoginView):
    form_class = LoginForm; template_name = "usuarios/login.html"; redirect_authenticated_user = True
    def get_success_url(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse("paneladmin:inicio")
        return super().get_success_url()
class LogoutUsuarioView(LogoutView): next_page = reverse_lazy("nucleo:inicio")
class RecuperarView(PasswordResetView):
    template_name = "registration/password_reset_form.html"; email_template_name = "registration/password_reset_email.html"; success_url = reverse_lazy("usuarios:recuperar_hecho")
