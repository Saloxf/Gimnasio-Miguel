from django.urls import path
from .views import ContactoView, InicioView
app_name = "nucleo"
urlpatterns = [
    path("", InicioView.as_view(), name="inicio"),
    path("contacto/", ContactoView.as_view(), name="contacto"),
]
