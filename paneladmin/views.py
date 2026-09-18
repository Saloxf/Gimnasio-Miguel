from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, UpdateView
from django.urls import reverse_lazy
from django import forms
from django.views.decorators.http import require_POST
from nucleo.mixins import AdminRequeridoMixin
from ejercicios.models import Ejercicio, GrupoMuscular
from rutinas.models import Rutina
from entrenamientos.models import SesionEntrenamiento, SerieEntrenamiento
class PanelInicioView(AdminRequeridoMixin, TemplateView):
    template_name = "paneladmin/inicio.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs); U = get_user_model()
        ctx.update({"usuarios_total": U.objects.count(), "usuarios_activos": U.objects.filter(is_active=True).count(), "ejercicios_total": SerieEntrenamiento.objects.values("ejercicio_id").distinct().count(), "sesiones_total": SesionEntrenamiento.objects.count()})
        return ctx

class EjerciciosPracticadosAdminView(AdminRequeridoMixin, TemplateView):
    template_name = "paneladmin/ejercicios_practicados.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        User = get_user_model()
        usuarios = []
        for usuario in User.objects.order_by("username"):
            ejercicios = Ejercicio.objects.filter(
                series_registradas__sesion__usuario=usuario
            ).distinct().select_related("grupo_muscular").order_by("nombre")
            if ejercicios.exists():
                usuarios.append({
                    "usuario": usuario,
                    "ejercicios": ejercicios,
                    "grupos": GrupoMuscular.objects.filter(
                        ejercicios__series_registradas__sesion__usuario=usuario
                    ).distinct().order_by("nombre"),
                    "total": ejercicios.count(),
                })
        ctx["usuarios_practica"] = usuarios
        ctx["total_ejercicios_practicados"] = SerieEntrenamiento.objects.values("ejercicio_id").distinct().count()
        return ctx
class UsuariosAdminView(AdminRequeridoMixin, ListView):
    template_name = "paneladmin/usuarios.html"; context_object_name = "usuarios"; paginate_by = 30
    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        users = get_user_model().objects.all().order_by("username")
        if query:
            users = users.filter(username__icontains=query) | users.filter(email__icontains=query)
        return users.distinct()

class UsuarioAdminForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        help_text="Máximo 150 caracteres. Solo letras, números y @/./+/-/_.",
    )
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(label="Nombre", required=False)
    last_name = forms.CharField(label="Apellidos", required=False)
    is_active = forms.BooleanField(
        label="Cuenta activa",
        required=False,
        help_text="Indica si el usuario puede acceder a CundiFit.",
    )
    is_staff = forms.BooleanField(
        label="Acceso administrativo",
        required=False,
        help_text="Permite acceder al panel de administración.",
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "is_active", "is_staff"]

class UsuarioEditarAdminView(AdminRequeridoMixin, UpdateView):
    model = get_user_model()
    form_class = UsuarioAdminForm
    template_name = "paneladmin/usuario_form.html"
    success_url = reverse_lazy("paneladmin:usuarios")

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado correctamente.")
        return super().form_valid(form)

@require_POST
def cambiar_estado_usuario(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user == request.user:
        messages.error(request, "No puedes desactivar tu propia cuenta.")
    else:
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])
        messages.success(request, "Estado del usuario actualizado.")
    return redirect("paneladmin:usuarios")

@require_POST
def eliminar_usuario(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user == request.user or user.is_superuser:
        messages.error(request, "Esta cuenta no puede eliminarse desde este panel.")
    else:
        user.delete()
        messages.success(request, "Usuario eliminado.")
    return redirect("paneladmin:usuarios")
