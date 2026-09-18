from django.urls import path
from .views import HistorialView, SesionDetailView, ActividadCreateView, ActividadDetailView, iniciar_entrenamiento, registrar_serie, finalizar_entrenamiento
app_name = "entrenamientos"
urlpatterns = [
    path("", HistorialView.as_view(), name="historial"), path("actividad/nueva/", ActividadCreateView.as_view(), name="actividad_nueva"), path("actividad/<int:pk>/", ActividadDetailView.as_view(), name="actividad"), path("iniciar/", iniciar_entrenamiento, name="iniciar"),
    path("iniciar/<int:rutina_id>/", iniciar_entrenamiento, name="iniciar_rutina"), path("sesion/<int:pk>/", SesionDetailView.as_view(), name="sesion"),
    path("sesion/<int:sesion_id>/serie/", registrar_serie, name="registrar_serie"), path("sesion/<int:pk>/finalizar/", finalizar_entrenamiento, name="finalizar"),
]
