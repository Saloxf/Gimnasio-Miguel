from django import forms
from .models import Rutina, EjercicioDeRutina
from ejercicios.models import Ejercicio
class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina; fields = ["nombre", "descripcion", "activa"]
    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if not nombre: raise forms.ValidationError("El nombre es obligatorio.")
        return nombre
class EjercicioDeRutinaForm(forms.ModelForm):
    class Meta:
        model = EjercicioDeRutina; fields = ["ejercicio", "orden", "series_objetivo", "repeticiones_objetivo", "peso_objetivo", "descanso_segundos"]
        labels = {"peso_objetivo": "Peso objetivo (kg)", "descanso_segundos": "Descanso (segundos)"}
        widgets = {"peso_objetivo": forms.NumberInput(attrs={"min": 0, "step": ".01"}), "series_objetivo": forms.NumberInput(attrs={"min": 1}), "repeticiones_objetivo": forms.NumberInput(attrs={"min": 1}), "descanso_segundos": forms.NumberInput(attrs={"min": 0})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.fields["ejercicio"].queryset = Ejercicio.objects.filter(activo=True)
class SerieRapidaForm(forms.Form):
    ejercicio = forms.ModelChoiceField(queryset=Ejercicio.objects.none(), widget=forms.HiddenInput)
    numero_serie = forms.IntegerField(min_value=1)
    peso = forms.DecimalField(min_value=0, max_digits=7, decimal_places=2)
    repeticiones = forms.IntegerField(min_value=1)
    def __init__(self, usuario, rutina, *args, **kwargs):
        super().__init__(*args, **kwargs); self.fields["peso"].label = "Peso (kg)"; self.fields["ejercicio"].queryset = Ejercicio.objects.filter(usos_en_rutinas__rutina=rutina)
