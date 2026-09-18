from django import forms
from .models import Ejercicio
class FiltroEjercicioForm(forms.Form):
    grupo = forms.IntegerField(required=False, widget=forms.HiddenInput)
    tipo = forms.ChoiceField(required=False, choices=[("", "Todos")] + Ejercicio.TIPOS)

class EjercicioPropioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ["nombre", "grupo_muscular", "tipo_ejercicio", "descripcion", "instrucciones", "equipamiento"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3}), "instrucciones": forms.Textarea(attrs={"rows": 4})}
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio.")
        return nombre
