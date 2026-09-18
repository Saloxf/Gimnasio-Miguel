from .models import RedSocial
def globales(request):
    return {"redes_sociales": RedSocial.objects.filter(activa=True)}
