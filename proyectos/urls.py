from django.urls import path

from .views import ProyectoView

urlpatterns = [
    # GET (lista) y POST (crear)
    path("", ProyectoView.as_view(), name="proyecto-lista"),
    # GET (detalle), PUT (actualizar) y DELETE (eliminar)
    path("<int:pk>/", ProyectoView.as_view(), name="proyecto-detalle"),
]
