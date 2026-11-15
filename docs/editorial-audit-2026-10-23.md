# Auditoría editorial — 23 de octubre de 2026

## Resumen

La publicación tiene una base técnica funcional, pero su sistema anterior confundía volumen publicado con interés demostrado. La automatización priorizaba noticias recientes de AdTech y Google; por diseño, el resultado no podía revelar si otros territorios atraerían una audiencia mayor.

La automatización `Pi Daily Editorial` quedó pausada. No se desplegaron cambios ni artículos nuevos durante esta auditoría.

## Línea de base

Período analizado: 25 de julio a 22 de octubre de 2026.

- 162 usuarios activos en todo el sitio.
- 188 sesiones en todo el sitio.
- 352 eventos `page_view`.
- Aproximadamente 63 sesiones y 117 vistas mensuales.
- 26 noticias publicadas hasta el 22 de octubre.
- Solo 8 noticias registraron alguna vista.
- 18 noticias no registraron vistas.
- Las noticias acumularon 18 vistas en total.
- Search Console registró 77 impresiones y 0 clics en el período exportado.

La primera meta editorial se fija en 1.000 sesiones mensuales de calidad. Es una meta de crecimiento, no una promesa para las primeras ocho semanas.

## Contenido

Hallazgos:

1. La selección anterior estaba concentrada en Ad Manager, GPT, navegador y operación técnica.
2. El supuesto mejor rendimiento de AdTech está sesgado por la cantidad publicada.
3. Los títulos suelen describir una función o proveedor antes que una consecuencia humana.
4. El contrato anterior exigía actualidad reciente incluso cuando una pieza durable podía ofrecer más valor.
5. El archivo se presenta como una biblioteca técnica conectada a productos, no todavía como un medio con identidad propia.

Acciones realizadas:

- Se definieron seis territorios equilibrados.
- Se habilitaron los formatos `analysis`, `case-study`, `essay`, `guide`, `interview` y `news`.
- Se creó un banco inicial de 60 ideas.
- Se creó un calendario experimental de 24 piezas durante ocho semanas.
- Se documentó una matriz de selección sobre 100 puntos con umbral 75.

## Medición

Antes de esta intervención, GA4 permitía observar páginas y eventos generales, pero no medía el comportamiento editorial con suficiente precisión.

Se incorporaron:

- `editorial_article_view`.
- `editorial_read_progress` al 25%, 50%, 75% y 90%.
- `editorial_engaged_time` a los 30, 60, 120 y 300 segundos activos.
- `editorial_to_pi` para el paso voluntario hacia secciones comerciales.
- Atribución de primera parte durante 30 días para `contact_start` y `contact_cta_click`.
- Señal local de lector editorial recurrente.

La exportación de analítica ahora puede generar un bloque separado para páginas editoriales.

Pendiente manual en GA4 Admin:

- Registrar las dimensiones personalizadas documentadas en `docs/analytics.md`.
- Definir o verificar exclusión de tráfico interno.
- Validar los eventos en Realtime y DebugView después del próximo despliegue.

## Indexación

La exportación estática contiene:

- 35 URLs editoriales en `sitemap-content.xml`.
- Las 35 URLs enlazadas desde la portada de Insights.
- Canonical, robots indexables y datos estructurados de artículo.
- Sitemap de noticias separado para las piezas de las últimas 48 horas.

Una comprobación externa encontró la portada de Insights y artículos individuales en resultados. Esto descarta un bloqueo general de indexación. La ausencia de páginas editoriales en el reporte exportado de Search Console puede combinar bajo volumen, anonimización de consultas y cobertura incompleta; debe revisarse URL por URL en la interfaz de Search Console.

## Experiencia y arquitectura

Decisión acordada:

- La publicación se comportará como un medio independiente.
- La landing comercial de Pi conservará servicios, casos y contacto.
- La firma de Pi será visible pero discreta.
- Los artículos no se convertirán en landings comerciales.

El rediseño visual no se inició porque depende de capturas de referencia que proporcionará la responsable del proyecto. El problema conocido —fondo gris y superficie de lectura poco cómoda— se resolverá dentro de ese prototipo, no mediante un cambio aislado sin dirección visual.

## Validación técnica

- JSON editorial válido.
- JavaScript válido.
- `manage.py check`: aprobado.
- 22 pruebas: aprobadas.
- Validación editorial de 35 artículos: aprobada.
- Exportación estática: 64 páginas HTML, 18 redirecciones, 7 sitemaps y 62 recursos.

## Próximos pasos

1. Recibir las capturas de referencias editoriales.
2. Diseñar y validar el prototipo de lectura.
3. Registrar dimensiones personalizadas en GA4.
4. Seleccionar y puntuar las primeras tres piezas del calendario.
5. Investigar y producir esas piezas sin publicarlas todavía.
6. Probar medición, distribución, visuales y lectura en móvil y escritorio.
7. Aprobar el inicio formal del piloto.

