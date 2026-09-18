from django import forms
from .models import SerieEntrenamiento, Actividad
class SerieForm(forms.ModelForm):
    class Meta:
        model = SerieEntrenamiento; fields = ["ejercicio", "numero_serie", "peso", "repeticiones", "descanso_segundos"]
        labels = {"peso": "Peso (kg)", "repeticiones": "Repeticiones", "descanso_segundos": "Descanso (segundos)"}
        widgets = {"peso": forms.NumberInput(attrs={"min": 0, "step": ".01", "inputmode": "decimal"}), "repeticiones": forms.NumberInput(attrs={"min": 1}), "numero_serie": forms.NumberInput(attrs={"min": 1})}
    def clean(self):
        data = super().clean()
        if data.get("peso") is not None and data["peso"] < 0: self.add_error("peso", "El peso no puede ser negativo.")
        return data

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ["nombre", "tipo", "realizada_en", "duracion_minutos", "distancia_km", "calorias", "notas", "archivo_gpx"]
        widgets = {
            "realizada_en": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "duracion_minutos": forms.NumberInput(attrs={"min": 1}),
            "distancia_km": forms.NumberInput(attrs={"min": 0, "step": ".01"}),
            "calorias": forms.NumberInput(attrs={"min": 0}),
            "notas": forms.Textarea(attrs={"rows": 3}),
            "archivo_gpx": forms.ClearableFileInput(attrs={"accept": ".gpx,application/gpx+xml"}),
        }
    def clean_duracion_minutos(self):
        value = self.cleaned_data["duracion_minutos"]
        if value < 1:
            raise forms.ValidationError("La duración debe ser mayor que cero.")
        return value
    def clean_archivo_gpx(self):
        archivo = self.cleaned_data.get("archivo_gpx")
        if archivo and not archivo.name.lower().endswith(".gpx"):
            raise forms.ValidationError("Solo se permiten archivos GPX.")
        if archivo and archivo.size > 10 * 1024 * 1024:
            raise forms.ValidationError("El archivo GPX no puede superar 10 MB.")
        return archivo
