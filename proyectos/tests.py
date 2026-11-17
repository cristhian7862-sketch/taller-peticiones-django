import json

from django.test import TestCase

from .models import Proyecto


class ProyectoViewTests(TestCase):
    def test_crud_completo(self):
        # POST -> CREATE
        r = self.client.post(
            "/proyectos/",
            data=json.dumps({"nombre": "Tienda", "descripcion": "E-commerce"}),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 201)
        pk = r.json()["id"]

        # GET -> READ (lista y detalle)
        self.assertEqual(len(self.client.get("/proyectos/").json()["proyectos"]), 1)
        self.assertEqual(self.client.get(f"/proyectos/{pk}/").json()["nombre"], "Tienda")

        # PUT -> UPDATE
        r = self.client.put(
            f"/proyectos/{pk}/",
            data=json.dumps({"nombre": "Tienda v2"}),
            content_type="application/json",
        )
        self.assertEqual(r.json()["nombre"], "Tienda v2")

        # DELETE -> DELETE
        self.assertEqual(self.client.delete(f"/proyectos/{pk}/").status_code, 200)
        self.assertFalse(Proyecto.objects.exists())
        self.assertEqual(self.client.get(f"/proyectos/{pk}/").status_code, 404)

    def test_post_sin_nombre(self):
        r = self.client.post("/proyectos/", data="{}", content_type="application/json")
        self.assertEqual(r.status_code, 400)
