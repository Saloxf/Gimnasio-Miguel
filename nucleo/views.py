from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView
from .forms import FormularioContacto
from .models import MensajeContacto
class InicioView(TemplateView):
    template_name = "nucleo/inicio.html"
class ContactoView(FormView):
    template_name = "nucleo/contacto.html"
    form_class = FormularioContacto
    success_url = "/contacto/"
    def form_valid(self, form):
        mensaje = form.save()
        send_mail(f"Contacto FitTrack: {mensaje.nombre}", mensaje.mensaje, mensaje.email, ["admin@fittrack.local"], fail_silently=True)
        messages.success(self.request, "Mensaje enviado. Te responderemos pronto.")
        return super().form_valid(form)
