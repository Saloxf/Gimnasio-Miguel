# CundiFit

CundiFit es una plataforma móvil-first para planificar rutinas, registrar series y
consultar progreso. Está construida con Django 5, plantillas server-side y una API
DRF, usando identificadores de código en español sin tildes.

## Funcionalidades

- Registro, inicio de sesión, cierre y recuperación de contraseña.
- Perfil físico, IMC informativo y objetivos personales.
- Biblioteca de ejercicios filtrable.
- CRUD de rutinas, ejercicios por rutina, duplicado y cálculo de volumen objetivo.
- Ejecución de sesiones: registro rápido de peso/repeticiones, volumen y finalización.
- Historial aislado por usuario, récords personales y gráfica Chart.js.
- Tablero con volumen semanal, sesiones y rutinas.
- API autenticada (`/api/rutinas/`, `/api/progreso/`, `/api/series/`).
- Panel propio protegido para personal de administración y `/admin/` de Django.
- Contacto por email (backend de consola en desarrollo), mensajes y redes editables.
- Interfaz responsive con glassmorphism, AOS, tema claro/oscuro persistente, menú
  offcanvas, navegación móvil, skeleton-ready, toasts, CTA sticky, favicon y botón
  volver arriba.
- Seguimiento de peso corporal con historial y gráfica.
- Ejercicios propios por usuario, visibles junto al catálogo general.
- Exportación e importación JSON de planes sin sobrescribir las rutinas existentes.
- Creación automática de récord personal cuando una serie supera las marcas previas.
- Registro manual de actividades de carrera, ciclismo, natación, caminata y otras,
  con duración, distancia, calorías y notas.
- API autenticada de actividades en `/api/actividades/`.
- Importación de GPX con validación de tamaño/extensión, recorrido sobre mapa
  Leaflet, elevación, desnivel, segmentos por kilómetro y ritmo estimado.
- Catálogo de 872 ejercicios de exercemus, con grupos musculares, categorías,
  instrucciones, equipo, alias, videos y datos de licencia.
- Integración opcional del dataset `hasaneyldrm/exercises-dataset` con 1.324
  ejercicios, miniaturas JPG y animaciones GIF enlazadas desde su repositorio.
- Quince plantillas prehechas: tres variantes por objetivo, filtrables por
  grupo muscular (Pecho, Espalda y Piernas) antes de copiarlas a las rutinas
  personales.

## Funciones avanzadas incorporadas desde OpenGym

La aplicación adapta al stack Django existente las funciones que no requieren
copiar la implementación original: registro de peso, biblioteca personal,
exportación/importación de planes, detección de récords y API para peso/progreso.
Los endpoints nuevos requieren sesión autenticada:

```text
GET/POST /api/peso/
GET      /api/plan/exportar/
POST     /api/plan/importar/
```

También están disponibles:

```text
/es/perfil/peso/
/es/ejercicios/nuevo/
```

## Funciones pendientes o condicionadas

- Passkeys requieren WebAuthn y HTTPS; el proyecto actual mantiene autenticación
  Django para desarrollo local.
- Notificaciones push requieren claves VAPID, service worker y un proveedor de
  entrega; no se activan silenciosamente en desarrollo.
- Coach con IA requiere una cuenta/proveedor externo y consentimiento explícito;
  no se incluye una llamada automática que pueda modificar rutinas.
- Importadores específicos de FitNotes, Strong, Hevy y Apple Health todavía no
  están implementados; la importación JSON propia sí está disponible.
- TCX y FIT quedan pendientes porque requieren
  parsers y pruebas con archivos de diferentes fabricantes.
- Superseries, ejercicios temporizados/cardio con métricas específicas, mapa
  muscular y APK nativo requieren ampliar el modelo y la interfaz de ejecución.

## Instalación local

Requiere Python 3.11+.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
py manage.py migrate
py manage.py importar_exercemus
py manage.py importar_exercises_dataset
py manage.py createsuperuser
py manage.py runserver
```

Abre `http://127.0.0.1:8000/`. El proyecto utiliza SQLite por defecto.
El comando `importar_exercemus` es idempotente: puede ejecutarse de nuevo para
actualizar el catálogo sin duplicarlo. El archivo de origen se encuentra en
`ejercicios/data/exercemus_exercises.json` y conserva la atribución/licencia del
proyecto original.

`importar_exercises_dataset` también es idempotente. Descarga el JSON oficial y
guarda las URLs versionadas de las imágenes/GIF, evitando añadir binarios
pesados al repositorio. Para usar una copia local o probar pocos registros:

```powershell
py manage.py importar_exercises_dataset --archivo ruta\exercises.json
py manage.py importar_exercises_dataset --limit 20
```

Los medios proceden de Gym visual y se muestran con la atribución/licencia
declarada por el dataset. Consulta su [LICENSE](https://github.com/hasaneyldrm/exercises-dataset/blob/main/LICENSE)
antes de desplegar la aplicación públicamente.

### Panel y credenciales de administrador

El panel interno está disponible en `/panel/` y requiere un usuario con
`is_staff` o `is_superuser`. Incluye búsqueda, edición, activación,
desactivación y eliminación protegida de usuarios. Para crear las credenciales
sin guardar contraseñas en el repositorio, define variables de entorno y ejecuta:

```powershell
$env:FITTRACK_ADMIN_USERNAME = "admin"
$env:FITTRACK_ADMIN_EMAIL = "admin@tu-dominio.com"
$env:FITTRACK_ADMIN_PASSWORD = "cambia-esta-clave"
py manage.py crear_administrador
```

El comando es idempotente y actualiza el administrador si ya existe. Cambia la
contraseña de ejemplo por una clave larga antes de usar el sistema.

## Entorno y producción

Todas las credenciales se leen desde `.env`; nunca se deben confirmar secretos.
`DATABASE_URL` acepta SQLite (`sqlite:///db.sqlite3`) o PostgreSQL, por ejemplo:

```text
DATABASE_URL=postgresql://usuario:clave@localhost:5432/fittrack
DEBUG=False
ALLOWED_HOSTS=fittrack.example.com
SECRET_KEY=una-clave-larga-y-aleatoria
```

Antes de desplegar:

```powershell
py manage.py check --deploy
py manage.py migrate
py manage.py collectstatic --noinput
gunicorn config.wsgi:application
```

WhiteNoise sirve los estáticos compilados y Gunicorn ejecuta WSGI. En producción
se recomienda HTTPS, `CSRF_TRUSTED_ORIGINS`, PostgreSQL y un proveedor SMTP.

### Despliegue recomendado en Render

El archivo `render.yaml` define un servicio web con Gunicorn y una base de
datos PostgreSQL. Para desplegarlo:

1. Sube el repositorio a GitHub.
2. En Render selecciona **New > Blueprint** y conecta este repositorio.
3. Confirma la creación de `cundifit` y `cundifit-db`.
4. Espera a que finalice el build; las migraciones, el catálogo de ejercicios,
   las rutinas prehechas y los archivos estáticos se procesan automáticamente.
5. En la consola del servicio define `FITTRACK_ADMIN_USERNAME`,
   `FITTRACK_ADMIN_EMAIL` y `FITTRACK_ADMIN_PASSWORD`, y ejecuta:

```bash
python manage.py crear_administrador
```

No guardes esas credenciales en GitHub. Después puedes cargar el catálogo y las
plantillas con los comandos de importación documentados anteriormente.

## Verificaciones

```powershell
py manage.py check
py manage.py makemigrations --check
py manage.py migrate
py manage.py test
```

Los querysets de las vistas de usuario siempre filtran por el usuario autenticado.
La API exige autenticación y la ejecución de una sesión verifica que la rutina y
los ejercicios pertenecen al usuario solicitante.
