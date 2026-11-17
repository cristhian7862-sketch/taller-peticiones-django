# LIBRERIAS
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Proyecto


# VISTA
@method_decorator(csrf_exempt, name="dispatch")
class ProyectoView(View):
    """
    Endpoint CRUD para Proyecto usando solo Django nativo.

    GET    /proyectos/          -> lista todos los proyectos      (READ)
    GET    /proyectos/<pk>/     -> obtiene un proyecto            (READ)
    POST   /proyectos/          -> crea un proyecto               (CREATE)
    PUT    /proyectos/<pk>/     -> actualiza un proyecto          (UPDATE)
    DELETE /proyectos/<pk>/     -> elimina un proyecto            (DELETE)
    """

    def get(self, request, pk=None):
        if pk is not None:
            proyecto = get_object_or_404(Proyecto, pk=pk)
            return JsonResponse(proyecto.to_dict())

        proyectos = [p.to_dict() for p in Proyecto.objects.all()]
        return JsonResponse({"proyectos": proyectos})

    def post(self, request, pk=None):
        if pk is not None:
            return JsonResponse({"error": "Para crear usa /proyectos/ sin id"}, status=405)
        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        nombre = datos.get("nombre")
        if not nombre:
            return JsonResponse({"error": "El campo 'nombre' es obligatorio"}, status=400)

        proyecto = Proyecto.objects.create(
            nombre=nombre,
            descripcion=datos.get("descripcion", ""),
        )
        return JsonResponse(proyecto.to_dict(), status=201)

    def put(self, request, pk=None):
        if pk is None:
            return JsonResponse({"error": "Indica el id: /proyectos/<id>/"}, status=400)
        proyecto = get_object_or_404(Proyecto, pk=pk)
        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        proyecto.nombre = datos.get("nombre", proyecto.nombre)
        proyecto.descripcion = datos.get("descripcion", proyecto.descripcion)
        proyecto.save()
        return JsonResponse(proyecto.to_dict())

    def delete(self, request, pk=None):
        if pk is None:
            return JsonResponse({"error": "Indica el id: /proyectos/<id>/"}, status=400)
        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return JsonResponse({"mensaje": f"Proyecto {pk} eliminado"})
