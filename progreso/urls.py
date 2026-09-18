from django.urls import path
from .views import ProgresoView
app_name = "progreso"
urlpatterns = [path("", ProgresoView.as_view(), name="inicio")]
