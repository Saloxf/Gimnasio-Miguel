from django import forms
from .models import Perfil, Objetivo, RegistroPeso
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil; exclude = ["usuario"]
        labels = {"altura_cm": "Altura (cm)", "peso_kg": "Peso corporal (kg)"}
        widgets = {
            "edad": forms.NumberInput(attrs={"min": 13, "max": 100, "placeholder": "Ej. 25"}),
            "altura_cm": forms.NumberInput(attrs={"min": 1, "step": ".01", "placeholder": "Ej. 175"}),
            "peso_kg": forms.NumberInput(attrs={"min": 1, "step": ".01", "placeholder": "Ej. 70"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.widget.attrs["class"] = "profile-input"
    def clean(self):
        data = super().clean()
        if data.get("edad") and not 13 <= data["edad"] <= 100: self.add_error("edad", "La edad debe estar entre 13 y 100.")
        for campo in ("altura_cm", "peso_kg"):
            if data.get(campo) is not None and data[campo] <= 0: self.add_error(campo, "Debe ser positivo.")
        return data
class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = Objetivo; fields = ["tipo_objetivo", "activo"]

class RegistroPesoForm(forms.ModelForm):
    class Meta:
        model = RegistroPeso
        fields = ["peso_kg", "notas"]
        labels = {"peso_kg": "Peso corporal (kg)"}
        widgets = {"peso_kg": forms.NumberInput(attrs={"min": "1", "step": ".01", "inputmode": "decimal", "placeholder": "70.00"})}
    def clean_peso_kg(self):
        peso = self.cleaned_data["peso_kg"]
        if peso <= 0:
            raise forms.ValidationError("El peso debe ser mayor que cero.")
        return peso
