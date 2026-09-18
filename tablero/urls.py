from django.urls import path
from .views import TableroView
app_name = "tablero"
urlpatterns = [path("", TableroView.as_view(), name="inicio")]
