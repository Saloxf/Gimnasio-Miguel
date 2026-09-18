from django.urls import path
from .views import *
app_name = "rutinas"
urlpatterns = [
    path("", RutinaListView.as_view(), name="lista"), path("nueva/", RutinaCreateView.as_view(), name="nueva"),
    path("<int:pk>/", RutinaDetailView.as_view(), name="detalle"), path("<int:pk>/editar/", RutinaUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", RutinaDeleteView.as_view(), name="eliminar"), path("<int:pk>/duplicar/", duplicar_rutina, name="duplicar"),
    path("plantillas/<int:pk>/usar/", usar_plantilla, name="usar_plantilla"),
    path("<int:rutina_id>/ejercicios/nuevo/", EjercicioRutinaCreateView.as_view(), name="ejercicio_nuevo"),
    path("ejercicios/<int:pk>/eliminar/", EjercicioRutinaDeleteView.as_view(), name="ejercicio_eliminar"),
]
