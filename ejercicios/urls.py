from django.urls import path
from .views import BibliotecaView, EjercicioDetailView, EjercicioPropioCreateView
app_name = "ejercicios"
urlpatterns = [
    path("", BibliotecaView.as_view(), name="biblioteca"),
    path("nuevo/", EjercicioPropioCreateView.as_view(), name="nuevo"),
    path("<int:pk>/", EjercicioDetailView.as_view(), name="detalle"),
]
