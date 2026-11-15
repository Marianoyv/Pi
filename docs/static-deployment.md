# Arquitectura y despliegue estático

Actualizado: 2026-08-22. Publicado y migrado al plan Spark.

## Resultado

El sitio público ya no necesita ejecutar Django por cada visita. Django queda como generador local y Firebase Hosting sirve una salida estática de aproximadamente 15 MB.

La generación incluye:

- Las páginas HTML comerciales, casos, productos y artículos públicos definidos por la fuente actual.
- 15 páginas de respaldo para enlaces antiguos.
- índice de sitemap y cinco secciones de sitemap.
- `robots.txt`, favicon y página 404.
- únicamente los 15 recursos estáticos referenciados por las páginas exportadas.

El antiguo rebuild, Design Lab, admin, base de datos y herramientas remotas ya fueron retirados del proyecto.

## Funciones en el navegador

Las tres herramientas públicas funcionan sin backend:

- UTM Builder valida y compone la URL localmente.
- Creative QA Checklist aplica reglas transparentes localmente.
- Creative Preview Lab analiza el marcado y lo muestra en un iframe aislado.

Los formularios muestran explícitamente que la información no se envía a un servidor. No hay llamadas `fetch` en el runtime de estas herramientas.

## Contacto

El sitio estático conserva email y WhatsApp. El formulario SMTP queda desactivado. Si se necesita recuperar el envío web en el futuro, debe implementarse como un endpoint pequeño y separado, con control de abuso y secretos fuera del navegador.

## Firebase Hosting

`firebase.json` apunta a `dist/`, mantiene las rutas con barra final, configura caché para recursos y define redirecciones permanentes para las URLs antiguas. El generador agrega además páginas HTML de redirección como respaldo para servidores locales que no apliquen esas reglas.

La publicación se realiza con:

```powershell
.\deploy-static.ps1
```

La versión estática fue publicada y verificada en `https://pidevelopment.web.app/`. Después de la verificación se eliminaron Cloud Run, los trabajos programados, Artifact Registry, los buckets antiguos, secretos y cuentas de servicio heredadas.

## Costos y recursos inactivos

Firebase Hosting y Cloud Storage no son el mismo almacenamiento. Hosting cobra según versiones almacenadas y transferencia desde su CDN. Un bucket de Cloud Storage vacío no almacena datos, pero cualquier objeto, operación o transferencia sí puede generar consumo según el plan vigente.

El proyecto quedó sin una cuenta de facturación vinculada y Firebase Hosting permanece disponible mediante el plan Spark. El código y la configuración local no pueden desplegar Cloud Run.

## Recuperación

- Django permanece únicamente como generador local de HTML.
- Firebase Hosting conserva historial de releases según su política de retención.
- Para incorporar un backend en el futuro, se debe añadir una API específica y separada; no conviene restaurar un rewrite global para todo el sitio.
