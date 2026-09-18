from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from django.urls import re_path
from django.views.generic import TemplateView

def redirigir_ruta_ingles(request, ruta=""):
    destino = "/es/" + ruta
    if request.META.get("QUERY_STRING"):
        destino += "?" + request.META["QUERY_STRING"]
    return HttpResponseRedirect(destino)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/", include("api.urls")),
    path("cuenta/", include("django.contrib.auth.urls")),
    re_path(r"^en(?:/(?P<ruta>.*))?/?$", redirigir_ruta_ingles),
]
urlpatterns += i18n_patterns(
    path("", include("nucleo.urls")),
    path("usuarios/", include("usuarios.urls")),
    path("perfil/", include("perfiles.urls")),
    path("ejercicios/", include("ejercicios.urls")),
    path("rutinas/", include("rutinas.urls")),
    path("entrenamientos/", include("entrenamientos.urls")),
    path("progreso/", include("progreso.urls")),
    path("tablero/", include("tablero.urls")),
    path("panel/", include("paneladmin.urls")),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
