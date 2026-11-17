# Taller – Peticiones en Django

**Curso:** Desarrollo de aplicaciones Web I – 4E
**Docente:** Jose Javier Torres Vanstrahlen

Endpoint CRUD hecho con **Django nativo** (sin Django REST Framework ni otras librerías externas), usando una **vista basada en clase** con los métodos `get()`, `post()`, `put()` y `delete()`.

---

## 1. ¿Cómo se crea un endpoint en Django nativo?

1. Se crea una clase que hereda de `django.views.View`.
2. Dentro se define un método por cada verbo HTTP (`get`, `post`, `put`, `delete`).
3. Se registra la clase en `urls.py` con `NombreView.as_view()`.
4. Cuando llega una petición, el método `dispatch()` de `View` mira `request.method` y llama al método con el mismo nombre en minúscula. Si el verbo no está definido, Django responde automáticamente **405 Method Not Allowed**.
5. Cada método devuelve un `HttpResponse` (en este caso `JsonResponse`, porque es una API).

## 2. Verbos HTTP y su relación con CRUD

| Verbo HTTP | Operación CRUD | Caso de uso | URL en este proyecto | Respuesta |
|---|---|---|---|---|
| **GET** | **R**ead (leer) | Consultar la lista de proyectos o uno solo. No modifica datos (es seguro e idempotente). | `GET /proyectos/` · `GET /proyectos/<pk>/` | 200 / 404 |
| **POST** | **C**reate (crear) | Registrar un proyecto nuevo con los datos enviados en el cuerpo. No es idempotente: enviarlo dos veces crea dos registros. | `POST /proyectos/` | 201 / 400 |
| **PUT** | **U**pdate (actualizar) | Modificar un proyecto existente identificado por su `pk`. Es idempotente. | `PUT /proyectos/<pk>/` | 200 / 400 / 404 |
| **DELETE** | **D**elete (eliminar) | Borrar un proyecto identificado por su `pk`. Es idempotente. | `DELETE /proyectos/<pk>/` | 200 / 404 |

> **Nota:** Django solo llena `request.POST` en peticiones POST con formularios. Para recibir JSON (y para PUT/DELETE) se lee el cuerpo crudo con `request.body` y se convierte con `json.loads()`.

## 3. Módulos, clases, funciones y decoradores usados

| Elemento | Se importa de | Descripción |
|---|---|---|
| `View` | `django.views` | Clase base de las vistas basadas en clase. Su método `dispatch()` envía cada petición al método que corresponde al verbo HTTP (`get`, `post`, `put`, `delete`). |
| `View.as_view()` | `django.views` | Convierte la clase en una función-vista que se puede poner en `urls.py`. |
| `JsonResponse` | `django.http` | Subclase de `HttpResponse` que convierte un diccionario de Python a JSON y pone la cabecera `Content-Type: application/json`. Permite indicar el código de estado con `status=`. |
| `HttpRequest` (`request`) | `django.http` | Objeto que recibe cada método. Se usaron `request.method` (verbo) y `request.body` (cuerpo crudo en bytes). |
| `get_object_or_404()` | `django.shortcuts` | Busca un objeto en la base de datos; si no existe lanza `Http404` y Django responde con 404. |
| `csrf_exempt` | `django.views.decorators.csrf` | Decorador que desactiva la verificación CSRF de la vista. Es necesario para que clientes como Postman o `curl` puedan hacer POST/PUT/DELETE sin token CSRF. *(En producción se debería usar otro mecanismo de autenticación.)* |
| `method_decorator` | `django.utils.decorators` | Convierte un decorador de funciones (como `csrf_exempt`) en uno que se puede aplicar a métodos de una clase. Con `name="dispatch"` se aplica a todos los verbos a la vez. |
| `path()` | `django.urls` | Define una ruta URL y la asocia a una vista. `<int:pk>` captura el id y lo pasa como argumento `pk`. |
| `include()` | `django.urls` | Incluye el `urls.py` de la app dentro del `urls.py` principal del proyecto. |
| `models.Model` y campos | `django.db.models` | Define la tabla `Proyecto` (ORM). Se usaron `objects.all()`, `objects.create()`, `.save()` y `.delete()` para el CRUD. |
| `json` | Librería estándar de Python | `json.loads()` convierte el cuerpo de la petición (texto JSON) en un diccionario. |

## 4. Archivos modificados

- [`proyectos/views.py`](proyectos/views.py) – vista `ProyectoView` con `get`, `post`, `put`, `delete`.
- [`proyectos/urls.py`](proyectos/urls.py) – rutas de la app (creado).
- [`config/urls.py`](config/urls.py) – incluye las rutas de la app.
- [`proyectos/models.py`](proyectos/models.py) – modelo `Proyecto`.
- [`config/settings.py`](config/settings.py) – se agregó `proyectos` a `INSTALLED_APPS`.
- [`proyectos/tests.py`](proyectos/tests.py) – pruebas de los 4 verbos.

## 5. Cómo ejecutarlo

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

Pruebas automáticas:

```bash
python manage.py test proyectos
```

Ejemplos con `curl`:

```bash
# Crear (POST)
curl -X POST http://127.0.0.1:8000/proyectos/ -H "Content-Type: application/json" -d "{\"nombre\": \"Tienda\", \"descripcion\": \"E-commerce\"}"

# Listar (GET)
curl http://127.0.0.1:8000/proyectos/

# Ver uno (GET)
curl http://127.0.0.1:8000/proyectos/1/

# Actualizar (PUT)
curl -X PUT http://127.0.0.1:8000/proyectos/1/ -H "Content-Type: application/json" -d "{\"nombre\": \"Tienda v2\"}"

# Eliminar (DELETE)
curl -X DELETE http://127.0.0.1:8000/proyectos/1/
```

## 6. Fuentes consultadas

- Django Documentation – *Class-based views*: https://docs.djangoproject.com/en/stable/topics/class-based-views/
- Django Documentation – *Base views (`View`, `dispatch`, `as_view`)*: https://docs.djangoproject.com/en/stable/ref/class-based-views/base/
- Django Documentation – *Request and response objects (`HttpRequest`, `JsonResponse`)*: https://docs.djangoproject.com/en/stable/ref/request-response/
- Django Documentation – *Django shortcut functions (`get_object_or_404`)*: https://docs.djangoproject.com/en/stable/topics/http/shortcuts/
- Django Documentation – *Decorating class-based views (`method_decorator`)*: https://docs.djangoproject.com/en/stable/topics/class-based-views/intro/#decorating-class-based-views
- Django Documentation – *Cross Site Request Forgery protection (`csrf_exempt`)*: https://docs.djangoproject.com/en/stable/ref/csrf/
- Django Documentation – *URL dispatcher (`path`, `include`)*: https://docs.djangoproject.com/en/stable/topics/http/urls/
- MDN Web Docs – *HTTP request methods*: https://developer.mozilla.org/es/docs/Web/HTTP/Methods
