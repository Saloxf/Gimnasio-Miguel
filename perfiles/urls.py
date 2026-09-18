from django.urls import path
from .views import PerfilView, ObjetivoListView, ObjetivoCreateView, ObjetivoUpdateView, ObjetivoDeleteView, RegistroPesoView
app_name = "perfiles"
urlpatterns = [
    path("", PerfilView.as_view(), name="perfil"),
    path("objetivos/", ObjetivoListView.as_view(), name="objetivos"),
    path("objetivos/nuevo/", ObjetivoCreateView.as_view(), name="objetivo_nuevo"),
    path("objetivos/<int:pk>/editar/", ObjetivoUpdateView.as_view(), name="objetivo_editar"),
    path("objetivos/<int:pk>/eliminar/", ObjetivoDeleteView.as_view(), name="objetivo_eliminar"),
    path("peso/", RegistroPesoView.as_view(), name="peso"),
]
