# Sistema editorial automático de Pi

> **Estado: pausado desde el 23 de octubre de 2026.** Este documento conserva el flujo diario anterior como referencia. La estrategia activa, los seis territorios y el piloto de ocho semanas están definidos en `docs/editorial-strategy.md`, `content/editorial/experiment.json` y `content/editorial/topic-bank.json`. No reactivar ni ejecutar este ciclo diario sin una decisión explícita posterior al piloto.

## Objetivo

Publicar una noticia diaria de extrema calidad para atraer tráfico orgánico calificado y convertir parte de esa atención en consultas para los servicios y productos de Pi Development.

La automatización no debe llenar una cuota a cualquier costo. Si no encuentra una noticia reciente, verificable, relevante y con una lectura propia útil, debe omitir la publicación del día. La confianza editorial vale más que la frecuencia.

Cada nota es un archivo JSON en `content/articles/` acompañado por una portada WebP original en `static/web/img/insights/`. Django la incorpora automáticamente al índice de Insights, la portada, su URL, los datos estructurados, los enlaces internos, el sitemap general y el sitemap de noticias durante sus primeras 48 horas. El formato canónico está en `content/templates/article.template.json`.

## Memoria compacta para Codex

Codex no debe volver a analizar todo el repositorio en cada ejecución. Antes de investigar lee solamente:

- `content/editorial/brief.json`: objetivo, audiencia, temas, puntaje de selección y contrato editorial.
- `content/editorial/sources.json`: fuentes oficiales de alta señal para iniciar la búsqueda.
- `content/editorial/index.json`: cobertura reciente y enlaces internos válidos.
- `content/templates/article.template.json`: estructura exacta del artículo.

`build-static.ps1` regenera el índice automáticamente después de cada publicación. Solo se abre un artículo anterior completo cuando el índice indica una posible duplicación que necesita comparación.

## Temas con intención de adquisición

La selección debe estar alineada con problemas por los que una empresa podría contratar a Pi:

- Cambios en Google Publisher Tag, Google Ad Manager, serving, refresh, viewability y monetización.
- Creative QA, formatos publicitarios, políticas técnicas y rendimiento de anuncios.
- Tracking, analytics, medición, atribución y calidad de datos.
- SEO técnico, Core Web Vitals, performance y comportamiento del navegador.
- Automatización, IA aplicada y software operativo cuando exista una conexión concreta con los servicios de Pi.

No se publican noticias generales de tecnología, resúmenes de tendencias ni novedades populares sin relación con una decisión técnica o comercial de la audiencia objetivo.

## Estándar editorial obligatorio

1. La noticia debe haber sido publicada o actualizada durante las últimas 72 horas. Se puede ampliar hasta siete días únicamente cuando el cambio siga siendo oportuno y todavía no exista una nota equivalente en Pi.
2. Debe existir al menos una fuente primaria accesible de la organización responsable y una confirmación independiente fiable cuando la afirmación sea controvertida, ambigua o tenga impacto legal o comercial relevante.
3. El título debe ser factual, específico y sin clickbait.
4. El artículo debe separar hechos confirmados, alcance no confirmado, análisis de Pi y acciones recomendadas.
5. Debe ofrecer una lectura original: impacto técnico, riesgos, prueba sugerida o decisión concreta. Un resumen de la fuente no alcanza.
6. Debe responder una intención de búsqueda real sin repetir mecánicamente palabras clave.
7. Debe enlazar únicamente productos, servicios o artículos de Pi que sean verdaderamente pertinentes.
8. No se inventan cifras, fechas, compatibilidad, citas, impacto, fuentes ni URLs.
9. No se copian párrafos de terceros.
10. Si la evidencia no alcanza, no se publica.
11. Toda noticia debe tener fecha y hora completas con zona horaria de Buenos Aires, firma editorial visible y una imagen original 16:9 de al menos 1200 píxeles de ancho.
12. La portada debe representar el tema concreto, funcionar como miniatura y evitar texto, logotipos, marcas de terceros, marcas de agua y estética genérica de stock.

## Prompt canónico para Codex

Ejecutá de forma autónoma el ciclo editorial diario de Pi Development en este proyecto. El objetivo es atraer tráfico orgánico calificado y generar oportunidades comerciales mediante una única noticia técnica, reciente y excepcionalmente útil. Leé y cumplí `docs/editorial-automation.md` antes de actuar y usá `content/templates/article.template.json` como contrato de contenido.

Investigá noticias publicadas o actualizadas durante las últimas 72 horas sobre AdTech, Google Publisher Tag o Ad Manager, creative QA, tracking y analytics, SEO o performance web, automatización, IA aplicada y software operativo. Elegí como máximo una historia. Priorizá cambios que afecten decisiones, riesgos, ingresos, calidad de implementación o trabajo operativo de publishers, AdOps, producto y tecnología. Evitá noticias generales, rumores, agregadores como fuente principal, contenido patrocinado sin valor técnico y temas ya cubiertos en `content/articles/`.

Exigí al menos una fuente primaria oficial y accesible. Sumá una confirmación independiente fiable si el tema es ambiguo, controvertido o tiene impacto legal o comercial importante. Contrastá fechas, versión, alcance y disponibilidad. Separá hechos confirmados, declaraciones del proveedor, inferencias y análisis de Pi. Si no existe una noticia suficientemente sólida, no publiques nada y explicá brevemente por qué se omitió la ejecución.

Cuando exista una historia válida, creá exactamente un archivo nuevo en `content/articles/` con el nombre `AAAA-MM-DD-slug.json` y una portada original en `static/web/img/insights/slug.webp`. Usá la generación de imágenes integrada para producir una ilustración editorial 16:9, de al menos 1200 píxeles de ancho, coherente con la paleta de Pi —marfil, cobalto, grafito y naranja señal—, sin texto, logotipos, marcas de terceros ni marcas de agua. Optimizala como WebP e incorporá una descripción accesible específica en `image_alt`. Si no podés producir una portada original válida, omití la publicación. No modifiques artículos anteriores, Python, HTML, CSS, JavaScript, rutas, dependencias, configuración, scripts ni el template. Si ya existe una publicación con la fecha local de hoy, verificála y no crees otra.

Escribí en español claro y profesional, con voz sobria, precisa y práctica. El artículo debe tener entre 500 y 1.800 palabras y contener: contexto verificable, qué cambió, a quién afecta, qué significa en una implementación real, riesgos o límites, qué revisar ahora, una lectura original de Pi, al menos tres conclusiones, al menos dos preguntas frecuentes y fuentes completas. El título y la descripción deben responder una intención de búsqueda real sin clickbait ni sobreoptimización. La nota debe ayudar a un lector técnico o decisor a comprender un cambio y reconocer que Pi puede diagnosticar, implementar o mejorar ese tipo de sistema, sin convertir el artículo en publicidad explícita.

Completá todos los campos del template. Usá `article_type: news`, registrá `published_datetime` y `updated_datetime` en ISO 8601 con offset `-03:00`, y usá `status: published` solamente después de terminar la revisión. Marcá al menos una fuente con `source_type: primary`. Usá únicamente slugs internos que ya existan y sean relevantes.

Antes de publicar, revisá precisión factual, coherencia de fechas, unicidad del slug y del tema, calidad de la fuente, ortografía, claridad, utilidad, enlaces y ausencia de afirmaciones sin respaldo. Ejecutá `manage.py check`, `manage.py validate_editorial`, las pruebas de `pi_development.web.test_static_export` y `build-static.ps1`. Si cualquier comprobación falla, corregí solamente el archivo creado hoy. No modifiques ni reviertas cambios ajenos.

Cuando todas las comprobaciones pasen, publicá automáticamente con `deploy-static.ps1`. Después comprobá por HTTP que la URL pública responda correctamente y contenga el título esperado. Al finalizar informá título, URL, intención de búsqueda, fuente principal, razón editorial para elegir el tema, validaciones y resultado del deploy. Si se omitió la publicación, informá la causa sin generar contenido de relleno.

## Operación

- Frecuencia: todos los días a las 08:00, hora de Buenos Aires.
- Volumen máximo: una noticia por día.
- Entorno: proyecto local de Pi Development.
- Publicación: Firebase Hosting mediante `deploy-static.ps1`.
- Condición: la computadora debe estar encendida, Codex abierto, Firebase CLI autenticado y `.venv` disponible.
- Seguridad: la validación editorial forma parte de `build-static.ps1`; un artículo que no cumple el contrato bloquea automáticamente el build y el deploy.
