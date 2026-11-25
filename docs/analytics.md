# Analítica de Pi Development

## Estado de esta entrega

La implementación del sitio está preparada para GA4 y Firebase Hosting. La configuración administrativa se aplicó y verificó en la sesión autorizada de Chrome el **24 de octubre de 2026**. La versión se publicó en Firebase Hosting ese mismo día; falta observar la llegada gradual de datos nuevos en Realtime, DebugView, audiencias e informes.

- Measurement ID instalado: `G-6XVTWEY4LW`.
- Propiedad confirmada: **Pi Development**, `342133855`; flujo web `4280290746`, `https://pidevelopment.web.app/`.
- Proyecto de publicación verificado: `pidevelopment`.
- La API de administración sigue deshabilitada; los ajustes se hicieron desde Analytics, sin ampliar los permisos de la cuenta de servicio.
- Inventario de ajustes aplicados y verificaciones: [analytics-ga4-setup.json](analytics-ga4-setup.json).
- Se crearon 24 dimensiones de evento, cinco métricas, cuatro audiencias y el evento clave `contact_start`, una vez por sesión y sin valor monetario predeterminado.
- Retención de eventos: 14 meses. Se conservó el filtro **Internal Traffic** en estado **Prueba**; no se inventaron direcciones IP ni se activaron exclusiones definitivas.
- Exploración privada guardada: **Pi Development — Contact journey**, con los pasos `page_view` → `plan_view` → `plan_select` → `contact_start`, desglose por dispositivo y tiempo transcurrido. Permite eventos intermedios y exige entrar por el primer paso.

## Qué mide el sitio

| Grupo | Eventos | Utilidad |
|---|---|---|
| Navegación | `page_view`, `navigation_click`, `section_jump`, `section_view` | Páginas, recorridos y secciones vistas |
| Interés comercial | `plan_view`, `plan_select`, `case_study_open`, `product_open` | Planes, casos y productos consultados |
| Contacto | `contact_cta_click`, `contact_start` | Intención de contacto por email, teléfono o WhatsApp y plan asociado |
| Herramientas | `tool_use`, `tool_error`, `tool_result_copy`, `utm_preset_select` | Uso real, errores de validación y resultados copiados |
| Contenido | `page_read_progress`, `page_engaged_time`, `editorial_article_view`, `editorial_read_progress`, `editorial_engaged_time`, `editorial_to_pi` | Profundidad, tiempo activo y paso del blog a servicios |
| Portfolio y video | `project_preview_open`, `video_start`, `video_progress`, `video_complete` | Vistas previas y videos iniciados por el visitante |
| Rendimiento real | `web_vital` | LCP, INP, CLS, FCP y TTFB, con valor, delta y clasificación |
| Salidas | `outbound_click` | Dominio de destino y ubicación del enlace, sin su URL completa |
| Interacción general | `control_click`, `form_start`, `form_submit`, `form_error`, `file_download`, `details_open` | Botones, formularios sin contenidos, descargas y detalles desplegados |

Un clic en WhatsApp **no confirma un lead ni una venta**. El sitio no inventa `generate_lead`, compras o ingresos. Los eventos de herramientas se envían después de que la operación correspondiente sucede, no por enviar un formulario vacío.

`page_view` se envía una sola vez por documento: sin cookies mientras el almacenamiento analítico está denegado y con almacenamiento sólo después de aceptarlo. Los porcentajes de lectura y los hitos de tiempo se registran una sola vez por página. El tiempo activo requiere una pestaña visible y enfocada. Las animaciones del hero y los videos decorativos con autoplay no se registran como interés comercial.

## Consentimiento, privacidad y pruebas locales

La medición no muestra un banner automáticamente: la etiqueta carga con `analytics_storage` permitido para recuperar el conteo normal de usuarios y sesiones. Publicidad, personalización publicitaria y Google Signals permanecen desactivados. Desde **Analytics & privacy** en el footer se puede mantener el almacenamiento analítico, cambiar a medición sin cookies o apagar la medición por completo. La preferencia dura hasta 180 días. Al apagarla se bloquean eventos posteriores y se eliminan las cookies GA y la atribución editorial propias del navegador.

Los eventos propios filtran parámetros no autorizados, emails, teléfonos y URLs completas. Las vistas eliminan query strings y fragmentos; la atribución UTM se conserva mediante campos de campaña filtrados. No se envían contenidos de formularios, mensajes, creatividades, URLs generadas en herramientas ni credenciales. El sitio guarda la atribución editorial durante 30 días sólo después de permitir almacenamiento analítico.

La **medición mejorada** quedó verificada: páginas, scroll, videos y descargas activos; salidas automáticas, búsqueda y formularios desactivados. Las interacciones equivalentes se miden con eventos propios filtrados, incluidos inicio, envío y error de formulario sin nombres de campos ni valores. Así se evita duplicar mediciones o capturar entradas de las herramientas. La cuenta tiene activada la ocultación de emails y de las 25 claves de consulta enumeradas en el JSON.

En localhost y dominios de preview no se carga la etiqueta ni se envían eventos a Google. Para revisar el funcionamiento local, abrir `http://127.0.0.1:8000/?analytics_debug=1`: los eventos quedan en `window.dataLayer`, **sin tráfico hacia GA4**, y el panel se puede abrir desde el footer. En producción, ese parámetro activa DebugView y sí envía eventos; no usarlo para navegar normalmente.

Los hosts de producción permitidos incluyen el dominio de `SITE_URL` y `ANALYTICS_ALLOWED_HOSTS` (por defecto `pidevelopment.web.app,pidevelopment.firebaseapp.com`). Un dominio nuevo debe configurarse también como dominio del sitio antes de publicar.

## Configuración aplicada en GA4 Admin

Las dimensiones y métricas del JSON quedaron registradas sin duplicados. `metric_id` y `link_text` no se registraron como dimensiones. Las métricas de lectura y video representan hitos; no se deben sumar como si fueran profundidad o tiempo total. `milestone_seconds` utiliza la unidad Segundos.

Las cuatro audiencias tienen una pertenencia de 30 días: **Business interest** (`plan_view` o `plan_select`, excluyendo temporalmente `contact_start`), **Contact intent** (`contact_start`), **Tool users** (`tool_use`) y **Engaged readers** (`editorial_engaged_time`, con `milestone_seconds ≥ 60` en ese evento). Se conservaron las audiencias predeterminadas y no se añadieron activadores de audiencia.

`contact_start` quedó marcado como evento clave contado una vez por sesión, sin importe ficticio. `contact_cta_click` no se marcó como una segunda conversión principal. No se enviaron eventos de prueba a producción para poblar reportes.

## Después de publicar

1. Verificar en Realtime y DebugView los tres estados: almacenamiento permitido, señales sin cookies y medición apagada. Debe haber una vista por carga en los dos primeros estados y ningún evento nuevo en el tercero.
2. Revisar el embudo y las audiencias cuando lleguen eventos de la nueva versión. Una audiencia sin usuarios antes de publicar es esperable. Analizar adquisición por país, dispositivo, canal y campaña con las dimensiones nativas de GA4.
3. Definir las IP reales de tráfico interno y comprobar primero los filtros en modo de prueba. No activar exclusiones hasta verificar qué visitas afectarían.

La propiedad de Search Console `https://pidevelopment.web.app/` está asociada con GA4, pero la cuenta de servicio local no tiene actualmente acceso a sus datos: la API responde 403. La tarea semanal lo registra como `unavailable` y continúa solo con GA4 hasta que un propietario conceda lectura. Las exportaciones a BigQuery siguen siendo opcionales. No se habilitaron Ads, Google Signals, vinculaciones publicitarias ni recursos facturables.

Las definiciones personalizadas no rellenan retroactivamente los informes y pueden tardar 24–48 horas en estar disponibles. CLS se expresa multiplicado por 1.000; los demás valores de rendimiento están en milisegundos. Para agregaciones de rendimiento usar el último valor por `metric_id`, no sumar los percentiles o promedios de todos los envíos.

## Validación y despliegue

`build-static.ps1` verifica la configuración, sintaxis JavaScript, pruebas de medición y del sitio, contenido editorial, exportación y dependencias finales. `scripts/check_static_release.py` rechaza una salida con el banner heredado, sin el panel de privacidad, sin Web Vitals o con entradas privadas. El paquete oficial `web-vitals` 6.2.3 está incluido localmente con su licencia e integridad verificada; no se necesita un CDN adicional.

```powershell
.\build-static.ps1
# Publicar sólo cuando se decida hacerlo:
.\deploy-static.ps1
```

Esta entrega se publicó el 24 de octubre de 2026 en `https://pidevelopment.web.app/`. El script de deploy regeneró y verificó el sitio antes de llamar a Firebase Hosting.

## Importar datos (acceso de sólo lectura)

El importador usa Google Analytics Data API y Search Console API. La cuenta de servicio conserva lectura de GA4; Search Console requiere que un propietario añada esa misma cuenta con acceso de lectura.

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = (Resolve-Path '.\credentials\analytics-reader.json').Path
$env:GA4_PROPERTY_ID = '342133855'
$env:SEARCH_CONSOLE_SITE_URL = 'https://pidevelopment.web.app/'
.\.venv\Scripts\python.exe manage.py import_analytics --days 28
```

La salida queda en `analytics/raw/AAAA-MM-DD/`, fuera de Git y del sitio generado. No publicar credenciales ni access tokens.

## Revisión editorial semanal

La tarea del domingo ejecuta dos importaciones: siete días para comparar la semana y 28 días para evitar decisiones basadas en oscilaciones pequeñas. Conserva los datos y el brief resultante en `analytics/weekly/`, una ruta local ignorada por Git y excluida del sitio.

El informe semanal sigue `content/templates/weekly-editorial-brief.template.md`. Resume rendimiento, revisiones a 48 horas/7 días/28 días y tres hipótesis para la semana siguiente. Los artículos de lunes, miércoles y viernes pueden usar esas señales, pero mantienen el umbral editorial, las fuentes y la posibilidad de no publicar.

La importación separa GA4 de Search Console para que una falta de permisos en una fuente no destruya los datos válidos de la otra. `latest-data.json` registra `available`, `partial` o `unavailable`; el brief debe mostrar esa limitación y no inferir consultas, impresiones o CTR cuando Search Console no esté disponible.

## Referencias oficiales

- [Consent Mode avanzado](https://support.google.com/analytics/answer/10000067)
- [Implementación de Consent Mode](https://developers.google.com/tag-platform/security/guides/consent)
- [Medición mejorada de GA4](https://support.google.com/analytics/answer/9216061?hl=en)
- [Dimensiones y métricas personalizadas](https://support.google.com/analytics/answer/14240153?hl=en)
- [Eventos recomendados y leads confirmados](https://developers.google.com/analytics/devguides/collection/ga4/reference/events)
- [Librería oficial Web Vitals](https://github.com/GoogleChrome/web-vitals)
