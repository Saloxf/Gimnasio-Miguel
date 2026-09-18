from django import forms
from django.core.mail import send_mail
from .models import MensajeContacto
class FormularioContacto(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ["nombre", "email", "mensaje"]
        widgets = {"mensaje": forms.Textarea(attrs={"rows": 5})}
    def clean_mensaje(self):
        valor = self.cleaned_data["mensaje"].strip()
        if len(valor) < 10: raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return valor
