# Pi Development

Sitio público estático generado desde Django y publicado en Firebase Hosting.

Producción: https://pidevelopment.web.app/ — plan Spark sin facturación vinculada.

## Arquitectura actual

- Django conserva el contenido, las plantillas, las rutas, el SEO y las pruebas como fuente de verdad local.
- `export_static` renderiza las páginas comerciales, casos, productos y artículos públicos, además de sitemap, robots, 404 y redirecciones de respaldo dentro de `dist/`.
- Firebase Hosting sirve directamente `dist/` desde su CDN; ya no reenvía cada visita a Cloud Run.
- UTM Builder, Creative QA Checklist y Creative Preview Lab se ejecutan en el navegador y no envían sus datos a un servidor.
- El contacto público usa email y WhatsApp. El envío SMTP permanece desactivado en la versión estática.
- El antiguo rebuild, Cloud Run, Docker, admin, base de datos, SMTP y herramientas remotas se eliminaron del proyecto.

## Abrir el proyecto localmente

La forma recomendada es hacer doble clic en `open-local.cmd` o ejecutar:

```powershell
.\open-local.ps1
```

El comando genera y valida `dist/`, reutiliza su propio servidor si ya existe, busca otro puerto si `8000` esta ocupado y abre el navegador. Sirve exactamente el paquete estatico que se publica en Firebase, evitando diferencias entre Django y produccion.

Opciones utiles:

```powershell
.\open-local.ps1 -SkipBuild   # apertura rapida con el dist existente
.\open-local.ps1 -NoBrowser  # inicia sin abrir una pestaña
.\open-local.ps1 -Stop       # detiene solo el servidor creado por este script
```

## Vista Django de la fuente

```powershell
.\.venv\Scripts\python.exe manage.py runserver --insecure
```

Esta vista existe únicamente para diagnostico de plantillas. Puede no servir assets con la configuracion estatica; para revisar el sitio completo se debe usar `open-local.ps1`. Produccion recibe solo los archivos de `dist/`.

## Generar el sitio estático

```powershell
.\build-static.ps1
```

El resultado se crea en `dist/`. Esa carpeta es regenerable y no se versiona.

Para revisar exactamente la configuración de Firebase Hosting:

```powershell
firebase emulators:start --only hosting --project pidevelopment
```

La versión estática local queda en `http://127.0.0.1:5000/`.

## Validación

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test pi_development.web.test_static_export
node --check static\web\js\browser-tools.js
```

## Analytics

El sitio registra clics de contacto y uso de herramientas en GA4. El comando `import_analytics` descarga datos de GA4 y Search Console mediante APIs de solo lectura, compara períodos equivalentes y genera CSV, JSON y un resumen Markdown local.

La medición usa Consent Mode avanzado sin banner automático: envía señales sin cookies por defecto, permite almacenamiento sólo por elección explícita y ofrece apagado total desde el footer. Incluye embudos comerciales, lectura, formularios sin contenidos, controles, descargas, herramientas y Core Web Vitals. Las visitas locales quedan fuera de GA4. La configuración de la cuenta se aplicó el 24/10/2026: dimensiones, métricas, audiencias, intención de contacto, retención y embudo. Falta validar la nueva versión en producción después del deploy.

Configuración y uso: [docs/analytics.md](docs/analytics.md). Inventario de la cuenta: [docs/analytics-ga4-setup.json](docs/analytics-ga4-setup.json).

La generación ejecuta pruebas y verifica que la salida incluya todas las dependencias de analítica y excluya archivos privados antes de permitir el deploy.

## Publicar en Firebase Hosting

```powershell
.\deploy-static.ps1
```

El script genera `dist/` antes de publicar y se detiene si la generación falla. El proyecto no contiene rewrites ni despliegues a Cloud Run. Los servicios, imágenes, compilaciones, buckets y secretos del backend anterior ya fueron retirados.

Los precios y cupos pueden cambiar; revisar siempre la documentación oficial antes de modificar el plan de facturación. Firebase Hosting contabiliza sus propias versiones almacenadas y la transferencia por CDN, de forma separada de un bucket de Cloud Storage.

Más detalles: [arquitectura y despliegue estático](docs/static-deployment.md).

