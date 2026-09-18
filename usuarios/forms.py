from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if get_user_model().objects.filter(email__iexact=email).exists(): raise forms.ValidationError("Este correo ya está registrado.")
        return email
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Tu nombre de usuario",
            "email": "tu@email.com",
            "first_name": "Nombre",
            "last_name": "Apellidos",
            "password1": "Mínimo 8 caracteres",
            "password2": "Repite tu contraseña",
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control", "placeholder": placeholders.get(name, field.label)})
            field.help_text = ""
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario o correo")

    def clean_username(self):
        identifier = self.cleaned_data["username"].strip()
        user_model = get_user_model()
        user = user_model.objects.filter(email__iexact=identifier).only("username").first()
        return user.username if user else identifier

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
