from django.contrib.auth.views import PasswordResetDoneView
from django.urls import path
from .views import RegistroView, LoginUsuarioView, LogoutUsuarioView, RecuperarView
app_name = "usuarios"
urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro"),
    path("login/", LoginUsuarioView.as_view(), name="login"),
    path("logout/", LogoutUsuarioView.as_view(), name="logout"),
    path("recuperar/", RecuperarView.as_view(), name="recuperar"),
    path("recuperar/hecho/", PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="recuperar_hecho"),
]
