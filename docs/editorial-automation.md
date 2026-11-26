# Sistema editorial medido de Pi

> **Estado: activo desde el 29 de noviembre de 2026.** El sistema recopila evidencia los domingos y puede publicar una pieza los lunes, miércoles y viernes a las 08:00, hora de Buenos Aires. La cadencia es un máximo, no una cuota.

## Objetivo

Construir audiencia recurrente con contenido original que explique una consecuencia humana, ayude a tomar una decisión y demuestre criterio propio. El sistema usa datos para formular mejores hipótesis; no convierte una muestra pequeña en una orden ni optimiza únicamente por visitas.

Cada nota vive en `content/articles/` y su portada en `static/web/img/insights/`. Django incorpora automáticamente las piezas publicadas al índice, sus URLs, datos estructurados, enlaces internos y sitemaps. El contrato canónico está en `content/templates/article.template.json`.

## Bucle semanal

### Domingo: evidencia y planificación

1. Ejecutar `scripts/collect-weekly-analytics.ps1` para importar GA4 y Search Console con acceso de solo lectura para los últimos 7 días y el contexto de 28 días.
2. Comparar la semana con el período anterior sin mezclar tráfico propio, despliegues o errores de medición con interés editorial. Si Search Console no tiene acceso, continuar con GA4 y declarar la limitación en vez de inventar demanda de búsqueda.
3. Revisar piezas a las 48 horas, 7 días y 28 días cuando exista muestra suficiente.
4. Consultar las fuentes de descubrimiento de `content/editorial/trend-sources.json`: Google Trends, agrupaciones de noticias, fuentes oficiales, medios y conversación pública. Las señales sociales descubren interés; nunca prueban hechos.
5. Guardar para cada candidato hora, mercado, dos señales distintas, saturación, vida útil y la pregunta que la cobertura todavía no responde.
6. Escribir `analytics/weekly/latest.md` con el formato de `content/templates/weekly-editorial-brief.template.md`.
7. Proponer una hipótesis distinta para lunes, miércoles y viernes. El brief no autoriza una publicación por sí solo.

`analytics/weekly/` es local, está fuera de Git y nunca se publica en Firebase.

### Lunes, miércoles y viernes: investigación y publicación

1. Leer `content/editorial/brief.json`, `content/editorial/sources.json`, `content/editorial/index.json`, `content/templates/article.template.json` y el brief semanal si tiene menos de ocho días.
2. Comprobar el uso disponible. Con menos de 35% en la ventana de cinco horas o menos de 25% en la semanal, conservar capacidad y no producir una pieza completa.
3. Revalidar dentro de las 72 horas previas las tendencias candidatas. Una señal caída, aislada o sin encaje descarta el tema.
4. Investigar temas recientes y piezas durables dentro de los seis territorios editoriales.
5. Puntuar cada candidato. Solo producir el mejor si supera 75/100 y no activa un rechazo obligatorio.
6. Mantener el artículo como borrador lógico durante investigación, redacción, verificación factual y producción visual. No generar la portada antes de aprobar tema y fuentes.
7. Ejecutar validación editorial, pruebas, build y deploy. Si cualquier control falla, no publicar.
8. Comprobar por HTTP la URL, el título, la imagen, las capas de verificación y la declaración visual.

Si no existe una historia sólida, el espacio queda vacío y la ejecución informa por qué.

## Contrato de noticia

La fórmula adoptada del sistema de Arcade World se expresa así para Pi. En noticias nuevas, las cuatro primeras capas aparecen separadas y visibles:

1. **Qué se anunció:** dato principal, responsable, fecha y alcance confirmado por la fuente primaria.
2. **Qué pudimos verificar:** contraste independiente, diferencias entre cifras y preguntas abiertas.
3. **Lectura editorial de Pi:** contexto o conclusión original, claramente separada de los hechos.
4. **Cómo verificamos esta noticia:** fuentes, señales de tendencia y controles superados.
5. **Qué conviene hacer:** prueba, decisión o señal que el lector puede revisar.
6. **Qué sigue abierto:** límites, desacuerdos y próximos hitos.

`summary` funciona como lectura rápida; `description` explica la consecuencia; `key_takeaways` debe incluir al menos una acción. Las noticias y los análisis nuevos requieren una fuente primaria y otra fuente independiente. Para afirmaciones sensibles se añaden tantas confirmaciones como sean necesarias.

## Política visual: apariencia de noticia, origen transparente

La portada predeterminada debe parecer producida para una publicación profesional: composición editorial realista, luz natural o físicamente creíble, materiales reconocibles, profundidad sobria y relación directa con el hecho. Debe evitar la estética genérica de “tecnología”: isometría 3D, neón, hologramas, circuitos decorativos, dashboards inventados o símbolos sin relación concreta.

Prioridad visual:

1. Fotografía propia o captura propia verificable, cuando exista y sea pertinente.
2. Composición editorial basada en materiales propios o con licencia.
3. Diagrama original cuando explica mejor el cambio.
4. Ilustración realista asistida por IA cuando no existe una imagen documental legítima.

Una imagen generada puede tener lenguaje fotográfico, pero nunca debe presentarse como registro documental de un hecho real. No recrea a una persona identificable realizando una acción que no ocurrió. Toda imagen asistida por IA incluye debajo de la portada: **“Ilustración editorial generada con IA. No es una fotografía documental del hecho.”**

Requisitos técnicos:

- Formato WebP, 16:9 y objetivo mínimo de 1536 × 864.
- Sin texto incrustado, logos, marcas de agua ni interfaces inventadas.
- Un sujeto o situación principal legible como miniatura.
- Color realista y edición sobria; la paleta de Pi puede aparecer como acento, no como filtro dominante.
- `image_alt` describe lo visible y `image_record` conserva creador, fecha, método, archivos de origen y declaración.

## Memoria compacta

Las ejecuciones no recorren todo el repositorio. Antes de investigar leen solamente los archivos compactos indicados arriba. Solo abren un artículo anterior completo si `index.json` señala una posible duplicación.

El domingo puede leer los archivos de `analytics/weekly/` y los datasets recién importados. Ninguna credencial, dato crudo o informe privado entra en `dist/`.

## Controles obligatorios

- Título factual, específico y sin clickbait.
- Hipótesis editorial y de distribución antes de producir.
- Hechos, declaraciones, inferencias y análisis separados.
- Evidencia de tendencia formada por dos señales públicas distintas y revalidada dentro de las 72 horas previas para toda noticia nueva.
- Comunicado oficial, contraste independiente, lectura editorial y pruebas de calidad presentados como capas visibles distintas.
- Fecha, zona horaria, autoría, fuentes y correcciones visibles.
- Entre 500 y 1.800 palabras; al menos tres conclusiones y dos preguntas frecuentes.
- Enlaces internos únicamente cuando sean pertinentes.
- Imagen original con procedencia documentada.
- `manage.py check`, `validate_editorial`, pruebas Django y JavaScript, exportación estática y verificación final aprobadas.
- Deploy automático únicamente después de superar todos los controles.

## Operación

- Revisión semanal: domingo 20:00, hora de Buenos Aires.
- Producción: lunes, miércoles y viernes a las 08:00, hora de Buenos Aires.
- Volumen máximo: una pieza por ejecución.
- Presupuesto: conservar al menos 35% de la ventana de cinco horas y 25% de la semanal; una sola pieza completa y una sola generación de portada por día.
- Publicación: Firebase Hosting mediante `deploy-static.ps1`.
- Entorno: computadora encendida, Codex abierto, Firebase CLI autenticado, `.venv` y credencial de analítica disponibles.
- Supervisión: toda ejecución deja un resumen; una falla de datos, validación o despliegue bloquea la publicación.
