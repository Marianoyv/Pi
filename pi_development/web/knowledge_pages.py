import json
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path


KNOWLEDGE_INDEX_PAGE = {
    "title": "Contenido técnico para AdTech, creatividades y tracking | Pi Development",
    "meta_description": "Base editorial técnica de Pi Development sobre validación de creatividades HTML, Google Publisher Tag, diagnóstico publicitario y URLs con parámetros UTM.",
    "meta_keywords": "contenido técnico adtech, validación de creatividades, google publisher tag, tracking utm",
    "eyebrow": "Contenido técnico",
    "h1": "Contenido técnico para AdTech, creatividades y tracking operativo",
    "description": "Esta base editorial reúne piezas técnicas cortas y útiles para revisar creatividades HTML, implementaciones con Google Publisher Tag y construcción de URLs con parámetros UTM sin convertir el sitio en un blog inflado.",
    "intro_title": "Qué tipo de contenido vas a encontrar",
    "intro": "Las páginas de conocimiento de Pi Development están pensadas para responder preguntas técnicas concretas y conectarlas con herramientas reales. El foco está en la utilidad inmediata, la estructura clara y la integración directa con la suite.",
    "support_title": "Cómo usar esta capa editorial",
    "support_text": "Podés entrar por problema técnico, por herramienta o por tema. Cada artículo enlaza herramientas relacionadas, guías SEO conectadas y otras lecturas útiles para que el contenido no quede aislado del producto.",
    "cta_title": "Hub principal de la suite",
    "cta_text": "Si necesitás una vista más operativa de toda la suite, la página central de herramientas AdTech sigue siendo la mejor entrada para conectar diagnóstico, QA, preview y tracking.",
    "cta_slug": "herramientas-adtech",
}

KNOWLEDGE_CLUSTER_ORDER = [
    "ia",
    "web-actual",
    "tecnologia-vida",
    "producto",
    "carrera",
    "adtech",
    "creatividades",
    "seo-performance",
    "tracking",
]

KNOWLEDGE_PAGE_DEFINITIONS = [
    {
        "status": "published",
        "article_type": "guide",
        "slug": "como-validar-una-creatividad-html-antes-de-publicarla",
        "title": "Cómo validar una creatividad HTML antes de publicarla | Pi Development",
        "meta_description": "Guía técnica para validar una creatividad HTML antes de publicarla: tamaño, peso, click path, scripts, iframes, audio, autoplay y diferencias entre preview y QA.",
        "meta_keywords": "validar creatividad html, validación de creatividades, qa técnico publicitario, preview de anuncios html",
        "eyebrow": "Creatividades",
        "cluster_key": "creatividades",
        "h1": "Cómo validar una creatividad HTML antes de publicarla",
        "description": "Una revisión inicial bien hecha evita que una creatividad llegue a publishing o trafficking con errores previsibles de dimensiones, click path, recursos externos o comportamiento multimedia.",
        "summary": "Guía técnica para revisar una creatividad HTML antes de publicarla y decidir si basta con preview, si hace falta QA o si la pieza todavía no está lista.",
        "search_intent": "Aprender qué revisar en una creatividad HTML antes de publicarla o enviarla a trafficking.",
        "business_relevance": "Un control previo reduce rechazos, fallos de serving y horas de diagnóstico en equipos creativos y de AdOps.",
        "target_audience": ["Equipos de Creative QA y AdOps", "Desarrolladores de creatividades HTML5"],
        "published_at": "2026-03-19",
        "updated_at": "2026-03-19",
        "published_datetime": "2026-03-19T20:44:14-03:00",
        "updated_datetime": "2026-03-19T20:44:14-03:00",
        "reading_time_minutes": 5,
        "image": "web/img/insights/validate-html-creative.webp",
        "image_alt": "Ilustración editorial de una creatividad HTML sometida a controles técnicos antes de su publicación.",
        "intro_paragraphs": [
            "Validar una creatividad HTML no es solo abrir el archivo y comprobar que algo renderiza. Antes de publicarla conviene revisar tamaño, peso, click path, recursos externos, comportamiento multimedia y cualquier dependencia que pueda alterar el serving real.",
            "Una primera pasada no reemplaza el QA final del ad server, pero sí reduce varios errores repetibles. También ayuda a decidir si basta con una vista previa controlada o si necesitás una checklist técnica más estricta antes de aprobar la pieza.",
        ],
        "key_takeaways": [
            "Comprobar dimensiones, peso y click path antes de revisar detalles visuales.",
            "Identificar scripts, iframes y recursos externos que dependan del entorno de serving.",
            "Separar una vista previa funcional del QA final requerido por la plataforma publicitaria.",
        ],
        "sections": [
            {
                "title": "Empezá por tamaño, peso y click path",
                "paragraphs": [
                    "Las primeras tres comprobaciones suelen ser las más simples y también las que más errores concentran: dimensiones correctas, peso razonable para el placement y una ruta de clic clara.",
                    "Si la creatividad no declara bien su tamaño o si el click path es ambiguo, no tiene sentido avanzar a una revisión más sofisticada sin corregir esa base.",
                ],
                "bullets": [
                    "Comprobá que el tamaño coincide con el placement previsto.",
                    "Verificá que el peso no llegue a niveles que compliquen la carga o la aprobación.",
                    "Asegurá que el click path sea claro: clickTag, macro o URL directa, pero no una mezcla dudosa.",
                ],
            },
            {
                "title": "Revisa scripts, iframes y dependencias externas",
                "paragraphs": [
                    "Scripts remotos, iframes, fuentes externas o recursos multimedia pueden hacer que una creatividad funcione en desarrollo y falle después en un entorno más restringido.",
                    "No siempre son un error en sí mismos, pero sí son una señal que conviene documentar antes de publicar para no confundir un problema del entorno con un problema del código.",
                ],
                "bullets": [
                    "Listá los recursos externos que la pieza necesita para renderizar.",
                    "Marcá los iframes y scripts de terceros que puedan quedar parciales en sandbox.",
                    "Aclará si hay macros o placeholders que dependen de un entorno propietario.",
                ],
            },
            {
                "title": "Audio, autoplay y comportamiento bloqueante",
                "paragraphs": [
                    "Autoplay con sonido, navegación fuera del frame o comportamiento invasivo suelen convertirse rápido en rechazo técnico o en una pieza bloqueada.",
                    "Esa capa conviene revisarla antes de hablar de polish visual porque afecta la aprobación, la experiencia de usuario y la compatibilidad con el contexto de serving.",
                ],
                "bullets": [
                    "Detectá autoplay con sonido o audio al cargar.",
                    "Comprobá que la pieza no intente escapar del frame.",
                    "Documentá cualquier comportamiento que dependa de interacción del usuario.",
                ],
            },
            {
                "title": "Preview y QA no son lo mismo",
                "paragraphs": [
                    "El preview sirve para responder si el markup renderiza de forma legible dentro de un contenedor controlado. El QA sirve para decidir si la pieza cumple criterios técnicos y si está lista para pasar al siguiente paso.",
                    "En una revisión inicial suelen convivir ambos: primero usás preview para ver el comportamiento visible y después una checklist para decidir si hay alertas o bloqueos reales.",
                ],
            },
            {
                "title": "Limitaciones de una revisión inicial",
                "paragraphs": [
                    "Una revisión inicial no replica SafeFrame, requests de red, clics reales ni el comportamiento final de un ad server. Su valor está en acotar problemas y separar lo evidente de lo que todavía requiere un entorno real.",
                    "Eso significa que una creatividad puede verse correcta en preview y aun así necesitar QA adicional, igual que puede quedar parcial en sandbox y seguir siendo válida dentro de un entorno propietario.",
                ],
            },
        ],
        "sources": [
            {
                "publisher": "IAB Tech Lab",
                "title": "HTML5 for Digital Advertising 2.0",
                "url": "https://iabtechlab.com/wp-content/uploads/2016/04/HTML5forDigitalAdvertising2.0.pdf",
                "accessed_at": "2026-09-10",
                "source_type": "primary",
            }
        ],
        "related_tool_slugs": ["creative-preview-lab", "creative-qa-checklist"],
        "related_seo_page_slugs": ["validar-creatividad-html", "preview-anuncios-html", "como-validar-tags-publicitarios"],
        "related_knowledge_slugs": [
            "errores-comunes-en-implementaciones-con-google-publisher-tag",
            "como-crear-urls-con-parametros-utm-correctamente",
        ],
        "faqs": [
            {
                "question": "¿Qué conviene revisar primero en una creatividad HTML?",
                "answer": "Dimensiones, peso, click path y dependencias externas. Esa base suele explicar buena parte de los fallos que después aparecen en serving o QA final.",
            },
            {
                "question": "¿Preview y QA técnico publicitario son lo mismo?",
                "answer": "No. El preview te muestra el comportamiento visible del markup. El QA técnico ordena criterios de aprobación y separa observaciones de bloqueos reales.",
            },
            {
                "question": "¿Una revisión inicial reemplaza el QA final del ad server?",
                "answer": "No. Sirve para llegar mejor preparado al entorno real, pero no sustituye la validación final en el contexto donde la pieza va a servir.",
            },
        ],
    },
    {
        "status": "published",
        "article_type": "guide",
        "slug": "errores-comunes-en-implementaciones-con-google-publisher-tag",
        "title": "Errores comunes en implementaciones con Google Publisher Tag | Pi Development",
        "meta_description": "Guía técnica sobre errores comunes en implementaciones con Google Publisher Tag: carga de GPT, slots, refresh, stack parcial y diferencias entre backend y navegador.",
        "meta_keywords": "google publisher tag, errores gpt, debug ads, diagnóstico técnico publicitario, herramientas para google publisher tag",
        "eyebrow": "AdTech",
        "cluster_key": "adtech",
        "h1": "Errores comunes en implementaciones con Google Publisher Tag",
        "description": "Muchos problemas atribuidos a Google Publisher Tag en realidad mezclan errores de carga, slots poco claros, refresh mal resuelto o lecturas incompletas del stack publicitario.",
        "summary": "Guía para detectar errores frecuentes en implementaciones con GPT y distinguir lo que puede leerse desde backend de lo que todavía requiere navegador.",
        "search_intent": "Identificar errores frecuentes de carga, slots y refresh en implementaciones con Google Publisher Tag.",
        "business_relevance": "Una implementación GPT legible y observable reduce impresiones perdidas, refresh inesperado y tiempo de diagnóstico.",
        "target_audience": ["Publishers y equipos de monetización", "Equipos de AdOps y desarrollo web"],
        "published_at": "2026-03-19",
        "updated_at": "2026-03-19",
        "published_datetime": "2026-03-19T20:44:14-03:00",
        "updated_datetime": "2026-03-19T20:44:14-03:00",
        "reading_time_minutes": 5,
        "image": "web/img/insights/gpt-implementation-errors.webp",
        "image_alt": "Ilustración editorial de una implementación publicitaria con slots, requests y señales de error bajo diagnóstico.",
        "intro_paragraphs": [
            "Cuando una página monetizada falla, Google Publisher Tag suele quedar en el centro del diagnóstico aunque el problema no siempre esté en la librería misma. A veces la carga es parcial, a veces los slots no son legibles y a veces el stack completo solo aparece en runtime.",
            "Por eso conviene ordenar primero los errores más comunes: carga visible de GPT, definición de slots, lógica de refresh y alcance real del análisis que hacés desde backend frente a lo que solo vas a confirmar en navegador.",
        ],
        "key_takeaways": [
            "Confirmar la carga de GPT antes de investigar inventario o refresh.",
            "Relacionar cada slot con su contenedor, tamaños y secuencia de requests.",
            "Usar el navegador para validar ejecución y no confundir señales del HTML con comportamiento real.",
        ],
        "sections": [
            {
                "title": "Errores de carga y presencia parcial de GPT",
                "paragraphs": [
                    "Lo primero es confirmar si la página expone señales compatibles con gpt.js o googletag en la respuesta inicial. Si esa base ni siquiera aparece, el problema no está en el refresh ni en el inventario, sino en la carga visible del stack.",
                    "También conviene documentar cuando la librería parece presente pero el resto del stack queda difuso. Esa combinación ya es una pista útil antes de pasar a una inspección más profunda.",
                ],
                "bullets": [
                    "GPT no visible en el HTML inicial.",
                    "Libreria visible, pero sin evidencia clara de slots o contenedores.",
                    "Carga mezclada con wrappers o vendors que vuelven opaco el diagnóstico.",
                ],
            },
            {
                "title": "Slots mal definidos o difíciles de rastrear",
                "paragraphs": [
                    "Una implementación puede cargar GPT y aun así dejar una estructura de slots muy poco legible. Eso complica el debug porque no queda claro dónde empieza el problema: inventario, naming de slots o contenedores montados del lado del cliente.",
                    "El objetivo de la primera pasada no es reconstruir todo el runtime, sino confirmar si el HTML inicial ya deja pistas suficientes sobre contenedores, iframes o placements.",
                ],
                "bullets": [
                    "Contenedores sin naming claro o difíciles de mapear.",
                    "Hints de slots inconsistentes con la estructura visible.",
                    "Iframes publicitarios visibles sin una relacion clara con el slot esperado.",
                ],
            },
            {
                "title": "Problemas de refresh y decisiones que dependen del runtime",
                "paragraphs": [
                    "El refresh suele discutirse como si fuera un detalle menor, pero puede estar ligado a triggers del navegador, lazy load, visibilidad de slots o lógica de wrappers.",
                    "Desde backend podés detectar algunas pistas, pero no conviene presentar esa lectura como si confirmara comportamiento real en runtime. El valor está en dejar claro cuándo el stack visible no alcanza para cerrar el diagnóstico.",
                ],
            },
            {
                "title": "Backend y navegador no responden la misma pregunta",
                "paragraphs": [
                    "El análisis backend sirve para detectar señales visibles, vendors, scripts, iframes y stack parcial en la respuesta inicial. El navegador sirve para validar ejecución, requests, callbacks y comportamiento real de carga.",
                    "Confundir ambas capas lleva a conclusiones pobres: o se sobreinterpreta una lectura backend o se entra al navegador sin una hipótesis clara sobre qué buscar.",
                ],
            },
        ],
        "sources": [
            {
                "publisher": "Google for Developers",
                "title": "Google Publisher Tag general best practices",
                "url": "https://developers.google.com/publisher-tag/guides/general-best-practices",
                "accessed_at": "2026-09-10",
                "source_type": "primary",
            },
            {
                "publisher": "Google for Developers",
                "title": "Control ad loading and refresh",
                "url": "https://developers.google.com/publisher-tag/guides/control-ad-loading",
                "accessed_at": "2026-09-10",
                "source_type": "primary",
            },
        ],
        "related_tool_slugs": ["adtech-debug-tool", "ai-auditor"],
        "related_seo_page_slugs": ["debug-gpt-ads", "debug-anuncios-web", "herramientas-adtech"],
        "related_knowledge_slugs": [
            "como-validar-una-creatividad-html-antes-de-publicarla",
            "como-crear-urls-con-parametros-utm-correctamente",
        ],
        "faqs": [
            {
                "question": "¿Una lectura backend alcanza para debuggear Google Publisher Tag?",
                "answer": "No por sí sola. Sirve para detectar señales visibles y ordenar hipótesis, pero el comportamiento real de carga y refresh sigue necesitando navegador.",
            },
            {
                "question": "¿Qué error se repite más en implementaciones con GPT?",
                "answer": "Es frecuente ver GPT visible sin una estructura clara de slots, o una mezcla de wrappers y vendors que vuelve opaca la lectura del inventario.",
            },
            {
                "question": "¿Cuándo conviene sumar AI Auditor a un debug de GPT?",
                "answer": "Cuando querés cruzar la capa publicitaria con el estado técnico general de la URL y confirmar si la página tiene otros problemas visibles que agravan el contexto.",
            },
        ],
    },
    {
        "status": "published",
        "article_type": "guide",
        "slug": "como-crear-urls-con-parametros-utm-correctamente",
        "title": "Cómo crear URLs con parámetros UTM correctamente | Pi Development",
        "meta_description": "Guía técnica para crear URLs con parámetros UTM correctamente: qué son, para qué sirven, errores comunes, naming limpio y ejemplos prácticos.",
        "meta_keywords": "cómo crear urls con parámetros utm, parámetros utm, utm builder, tracking utm",
        "eyebrow": "Tracking",
        "cluster_key": "tracking",
        "h1": "Cómo crear URLs con parámetros UTM correctamente",
        "description": "Las UTMs parecen simples, pero varios errores de tracking empiezan antes de analytics: naming inconsistente, sobrescritura de queries, URLs rotas o parámetros agregados sin criterio.",
        "summary": "Guía técnica para construir URLs con UTMs limpias, preservar la URL base y evitar errores operativos antes de compartir una campaña.",
        "search_intent": "Aprender a crear URLs con parámetros UTM sin romper la URL de destino ni fragmentar la medición.",
        "business_relevance": "Una taxonomía consistente mejora la atribución y evita campañas difíciles de comparar en Analytics.",
        "target_audience": ["Equipos de marketing y analítica", "Equipos de trafficking y operaciones"],
        "published_at": "2026-03-19",
        "updated_at": "2026-03-19",
        "published_datetime": "2026-03-19T20:44:14-03:00",
        "updated_datetime": "2026-03-19T20:44:14-03:00",
        "reading_time_minutes": 4,
        "image": "web/img/insights/clean-utm-urls.webp",
        "image_alt": "Ilustración editorial de parámetros de campaña organizados que conservan intacta una URL de destino.",
        "intro_paragraphs": [
            "Los parámetros UTM sirven para identificar fuente, medio, campaña y otros detalles de una URL que va a circular en medios, email, paid social u otros canales operativos.",
            "El problema es que muchas veces se agregan a mano, sin preservar query params existentes y sin una convención mínima de naming. El resultado es una URL poco legible, difícil de comparar y fácil de romper.",
        ],
        "key_takeaways": [
            "Preservar los parámetros funcionales que ya existen en la URL de destino.",
            "Aplicar una convención estable para source, medium y campaign.",
            "Validar la URL final completa antes de compartirla o activarla en una campaña.",
        ],
        "sections": [
            {
                "title": "Qué son las UTMs y para qué sirven",
                "paragraphs": [
                    "Las UTMs son parámetros que se agregan a una URL para identificar de dónde viene el tráfico y bajo qué criterio operativo fue compartida esa dirección.",
                    "No son una capa de SEO ni una solución mágica de analítica. Su utilidad está en dejar más claro el origen de la visita y en sostener una lectura consistente entre equipos.",
                ],
                "bullets": [
                    "utm_source para identificar la fuente.",
                    "utm_medium para indicar el tipo de canal o medio.",
                    "utm_campaign para nombrar la iniciativa o contexto operativo.",
                    "utm_term y utm_content solo cuando realmente aportan claridad.",
                ],
            },
            {
                "title": "Errores comunes al construir URLs con UTM",
                "paragraphs": [
                    "Los errores más frecuentes no son complejos: repetir claves, sobrescribir parámetros que ya estaban en la URL, inventar nomenclaturas nuevas en cada campaña o compartir una URL final que nadie revisó completa.",
                    "También es habitual usar nombres demasiado largos o poco consistentes, lo que vuelve más difícil comparar resultados después.",
                ],
                "bullets": [
                    "Romper query params existentes al pegar UTMs a mano.",
                    "Usar source, medium o campaign con naming distinto para el mismo caso.",
                    "Agregar parámetros opcionales sin una razón clara.",
                    "No comprobar la URL final completa antes de compartirla.",
                ],
            },
            {
                "title": "Naming limpio y legible",
                "paragraphs": [
                    "Un naming limpio no significa burocracia. Significa que alguien más del equipo pueda leer la URL final y entender con bastante rapidez de qué canal y campaña se trata.",
                    "Si cada persona inventa una convención nueva, las UTMs dejan de ser una ayuda operativa y se convierten en ruido.",
                ],
                "bullets": [
                    "Mantener source y medium en minúsculas y sin espacios.",
                    "Usar campaign con criterio estable entre acciones comparables.",
                    "Evitar palabras vagas o internas que después nadie entiende fuera del contexto inmediato.",
                ],
            },
            {
                "title": "Ejemplos prácticos",
                "paragraphs": [
                    "Una URL como https://example.com/landing puede pasar a https://example.com/landing?utm_source=newsletter&utm_medium=email&utm_campaign=lanzamiento-q2 si la acción es un envío editorial.",
                    "Si la URL base ya trae parámetros funcionales, por ejemplo ref=home, conviene preservarlos y agregar las UTMs sin destruir esa parte de la dirección.",
                ],
            },
        ],
        "sources": [
            {
                "publisher": "Google Analytics Help",
                "title": "URL builders: Collect campaign data with custom URLs",
                "url": "https://support.google.com/analytics/answer/10917952?hl=en",
                "accessed_at": "2026-09-10",
                "source_type": "primary",
            }
        ],
        "related_tool_slugs": ["utm-builder"],
        "related_seo_page_slugs": ["como-crear-utms", "analizar-seo-pagina", "herramientas-adtech"],
        "related_knowledge_slugs": [
            "como-validar-una-creatividad-html-antes-de-publicarla",
            "errores-comunes-en-implementaciones-con-google-publisher-tag",
        ],
        "faqs": [
            {
                "question": "¿Conviene escribir URLs con UTM a mano?",
                "answer": "Solo si el caso es muy simple y aun así revisás la URL final completa. En flujos reales conviene un builder que preserve parámetros y reduzca errores manuales.",
            },
            {
                "question": "¿UTM Builder reemplaza una convención de naming?",
                "answer": "No. Ayuda a construir la URL con más consistencia, pero el criterio de naming sigue dependiendo del equipo y del uso que le van a dar a esos parámetros.",
            },
            {
                "question": "¿Las UTMs afectan la landing que recibe tráfico?",
                "answer": "Pueden afectar la URL operativa y la forma en que circula la página, por eso tiene sentido revisar tanto el etiquetado como la calidad técnica de la landing final cuando hace falta.",
            },
        ],
    },
]


ARTICLE_CONTENT_DIR = Path(__file__).resolve().parents[2] / "content" / "articles"
REQUIRED_ARTICLE_FIELDS = {
    "article_type",
    "slug",
    "title",
    "meta_description",
    "eyebrow",
    "cluster_key",
    "h1",
    "description",
    "summary",
    "search_intent",
    "business_relevance",
    "target_audience",
    "intro_paragraphs",
    "published_datetime",
    "image",
    "image_alt",
    "sections",
}


def _load_file_articles():
    """Load automation-friendly editorial entries without changing Python code."""
    if not ARTICLE_CONTENT_DIR.exists():
        return []

    articles = []
    seen_slugs = {page["slug"] for page in KNOWLEDGE_PAGE_DEFINITIONS}
    for article_path in sorted(ARTICLE_CONTENT_DIR.glob("*.json")):
        article = json.loads(article_path.read_text(encoding="utf-8"))
        missing_fields = REQUIRED_ARTICLE_FIELDS.difference(article)
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Editorial article {article_path.name} is missing: {missing}")
        if article["slug"] in seen_slugs:
            raise ValueError(f"Duplicate editorial slug: {article['slug']}")
        if article.get("status", "published") != "published":
            continue
        seen_slugs.add(article["slug"])
        articles.append(article)
    return articles


KNOWLEDGE_PAGE_DEFINITIONS.extend(_load_file_articles())


def get_knowledge_index_page():
    return deepcopy(KNOWLEDGE_INDEX_PAGE)


def get_knowledge_page(slug):
    for page in KNOWLEDGE_PAGE_DEFINITIONS:
        if page["slug"] == slug:
            return deepcopy(page)
    return None


def get_public_knowledge_slugs():
    return [page["slug"] for page in KNOWLEDGE_PAGE_DEFINITIONS]


def get_latest_knowledge_pages(limit=3):
    pages = [deepcopy(page) for page in KNOWLEDGE_PAGE_DEFINITIONS]
    pages.sort(
        key=lambda page: (page.get("published_datetime") or page.get("published_at") or "", page["slug"]),
        reverse=True,
    )
    return pages[:limit]


def get_recent_news_articles(reference_datetime=None):
    reference_datetime = reference_datetime or datetime.now(timezone.utc)
    cutoff = reference_datetime - timedelta(days=2)
    articles = []
    for page in KNOWLEDGE_PAGE_DEFINITIONS:
        if page.get("article_type") != "news" or not page.get("published_datetime"):
            continue
        published = datetime.fromisoformat(page["published_datetime"])
        if cutoff <= published.astimezone(timezone.utc) <= reference_datetime:
            articles.append(deepcopy(page))
    articles.sort(key=lambda page: page["published_datetime"], reverse=True)
    return articles


def get_related_knowledge_pages(slugs):
    pages = []
    for slug in slugs:
        page = get_knowledge_page(slug)
        if page:
            pages.append(page)
    return pages


def get_knowledge_listing_groups():
    groups = []
    for cluster_key in KNOWLEDGE_CLUSTER_ORDER:
        pages = [deepcopy(page) for page in KNOWLEDGE_PAGE_DEFINITIONS if page.get("cluster_key") == cluster_key]
        pages.sort(key=lambda page: (page.get("published_at", ""), page["slug"]), reverse=True)
        if pages:
            groups.append({"cluster_key": cluster_key, "pages": pages})
    return groups
