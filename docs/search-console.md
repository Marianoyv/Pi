# Google Search Console — Pi Development

Revisión realizada el 24 de octubre de 2026 sobre la propiedad de prefijo de URL `https://pidevelopment.web.app/`.

## Estado verificado

- Propietario verificado; la propiedad está asociada con Google Analytics 4, propiedad y flujo **Pi Development**.
- `robots.txt` figura válido en Search Console y responde `200` en producción.
- `sitemap.xml` responde `200` como índice XML y enlaza los sitemaps por sección generados por el proyecto.
- Search Console muestra una página indexada, ninguna página excluida y ningún problema de indexación detectado en los últimos 90 días. Este informe todavía no refleja las 64 páginas de la versión preparada.
- No hay acciones manuales ni problemas de seguridad.
- No hay suficientes datos de campo para Core Web Vitals.
- En los últimos 90 días hubo 261 solicitudes de rastreo, 316 ms de respuesta media y 842 KB descargados.
- El host tiene disponibilidad aceptable en la actualidad. Google registró problemas de conectividad en el pasado.
- El historial de rastreo está dominado por respuestas antiguas: 44 % `404`, 36 % `301`, 19 % `200` y menos de 1 % `5xx`. La nueva arquitectura conserva redirecciones y debe reducir esos errores una vez rastreada.

## Acciones realizadas

Después del despliegue del 24 de octubre de 2026 se volvió a enviar `sitemap.xml`. Search Console confirmó que el sitemap se envió correctamente y que lo procesará periódicamente. La portada ya figura indexada y se solicitó un nuevo rastreo para que Google revise la versión publicada.

El estado detallado del sitemap todavía puede mostrar temporalmente el resultado anterior **No se ha podido leer el sitemap** mientras Google vuelve a procesarlo. Se comprobó de forma independiente que el índice y sus seis sitemaps secundarios responden `200`, usan `application/xml` y contienen XML válido. Los registros antiguos de `/robots.txt` y `/sitemaps.txt` no son sitemaps válidos; no deben reenviarse.

Después del envío, Google debe volver a leer el índice y descubrir sus secciones. La indexación no es instantánea ni garantizada. Tras publicar cualquier cambio, conviene inspeccionar la portada, solicitar su indexación y vigilar páginas descubiertas, códigos `404`, Core Web Vitals y consultas durante los días siguientes.
