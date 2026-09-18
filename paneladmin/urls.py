from django.urls import path
from .views import PanelInicioView, UsuariosAdminView, UsuarioEditarAdminView, EjerciciosPracticadosAdminView, cambiar_estado_usuario, eliminar_usuario
app_name = "paneladmin"
urlpatterns = [path("", PanelInicioView.as_view(), name="inicio"), path("usuarios/", UsuariosAdminView.as_view(), name="usuarios"), path("ejercicios-practicados/", EjerciciosPracticadosAdminView.as_view(), name="ejercicios_practicados"), path("usuarios/<int:pk>/editar/", UsuarioEditarAdminView.as_view(), name="usuario_editar"), path("usuarios/<int:pk>/estado/", cambiar_estado_usuario, name="usuario_estado"), path("usuarios/<int:pk>/eliminar/", eliminar_usuario, name="usuario_eliminar")]
