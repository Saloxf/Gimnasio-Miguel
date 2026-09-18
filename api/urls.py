from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RutinaViewSet, resumen_progreso, registrar_serie_api, peso_api, exportar_plan, importar_plan, actividades_api
app_name = "api"
router = DefaultRouter(); router.register("rutinas", RutinaViewSet, basename="rutina")
urlpatterns = [path("", include(router.urls)), path("progreso/", resumen_progreso, name="progreso"), path("series/", registrar_serie_api, name="serie"), path("peso/", peso_api, name="peso"), path("actividades/", actividades_api, name="actividades"), path("plan/exportar/", exportar_plan, name="exportar_plan"), path("plan/importar/", importar_plan, name="importar_plan")]
