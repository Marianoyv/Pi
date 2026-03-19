from copy import deepcopy


KNOWLEDGE_INDEX_PAGE = {
    "title": "Contenido tecnico para AdTech, creatividades y tracking | Pi Development",
    "meta_description": "Base editorial tecnica de Pi Development sobre validacion de creatividades HTML, Google Publisher Tag, diagnostico publicitario y URLs con parametros UTM.",
    "meta_keywords": "contenido tecnico adtech, validacion de creatividades, google publisher tag, tracking utm",
    "eyebrow": "Contenido tecnico",
    "h1": "Contenido tecnico para AdTech, creatividades y tracking operativo",
    "description": "Esta base editorial reune piezas tecnicas cortas y utiles para revisar creatividades HTML, implementaciones con Google Publisher Tag y construccion de URLs con parametros UTM sin convertir el sitio en un blog inflado.",
    "intro_title": "Que tipo de contenido vas a encontrar",
    "intro": "Las knowledge pages de Pi Development estan pensadas para responder preguntas tecnicas concretas y conectarlas con tools reales. El foco esta en utilidad inmediata, estructura clara e integracion directa con la suite.",
    "support_title": "Como usar esta capa editorial",
    "support_text": "Puedes entrar por problema tecnico, por herramienta o por tema. Cada articulo enlaza a tools relacionadas, guias SEO conectadas y otras lecturas utiles para que el contenido no quede aislado del producto.",
    "cta_title": "Hub principal de la suite",
    "cta_text": "Si necesitas una vista mas operativa de toda la suite, la pagina hub de herramientas AdTech sigue siendo la mejor entrada para conectar diagnostico, QA, preview y tracking.",
    "cta_slug": "herramientas-adtech",
}

KNOWLEDGE_CLUSTER_ORDER = [
    "adtech",
    "creatividades",
    "tracking",
]

KNOWLEDGE_PAGE_DEFINITIONS = [
    {
        "slug": "como-validar-una-creatividad-html-antes-de-publicarla",
        "title": "Cómo validar una creatividad HTML antes de publicarla | Pi Development",
        "meta_description": "Guia tecnica para validar una creatividad HTML antes de publicarla: tamano, peso, click path, scripts, iframes, audio, autoplay y diferencias entre preview y QA.",
        "meta_keywords": "validar creatividad html, validacion de creatividades, qa tecnico publicitario, preview de anuncios html",
        "eyebrow": "Creatividades",
        "cluster_key": "creatividades",
        "h1": "Cómo validar una creatividad HTML antes de publicarla",
        "description": "Una revision inicial bien hecha evita que una creatividad llegue a publishing o trafficking con errores previsibles de dimensiones, click path, recursos externos o comportamiento multimedia.",
        "summary": "Guia tecnica para revisar una creatividad HTML antes de publicarla y decidir si basta con preview, si hace falta QA o si la pieza todavia no esta lista.",
        "intro_paragraphs": [
            "Validar una creatividad HTML no es solo abrir el archivo y comprobar que algo renderiza. Antes de publicarla conviene revisar tamano, peso, click path, recursos externos, comportamiento multimedia y cualquier dependencia que pueda alterar el serving real.",
            "Una primera pasada no reemplaza el QA final del ad server, pero si reduce varios errores repetibles. Tambien ayuda a decidir si basta con una vista previa controlada o si necesitas una checklist tecnica mas estricta antes de aprobar la pieza.",
        ],
        "sections": [
            {
                "title": "Empieza por tamano, peso y click path",
                "paragraphs": [
                    "Las primeras tres comprobaciones suelen ser las mas simples y tambien las que mas errores concentran: dimensiones correctas, peso razonable para el placement y una ruta de clic clara.",
                    "Si la creatividad no declara bien su tamano o si el click path es ambiguo, no tiene sentido avanzar a una revision mas sofisticada sin corregir esa base.",
                ],
                "bullets": [
                    "Comprueba que el tamano coincide con el placement previsto.",
                    "Verifica que el peso no se vaya a niveles que compliquen carga o aprobacion.",
                    "Asegura que el click path sea claro: clickTag, macro o URL directa, pero no una mezcla dudosa.",
                ],
            },
            {
                "title": "Revisa scripts, iframes y dependencias externas",
                "paragraphs": [
                    "Scripts remotos, iframes, fuentes externas o recursos multimedia pueden hacer que una creatividad funcione en desarrollo y falle despues en un entorno mas restringido.",
                    "No siempre son un error en si mismos, pero si son una senal que conviene documentar antes de publicar para no confundir un problema del entorno con un problema del codigo.",
                ],
                "bullets": [
                    "Lista recursos externos que la pieza necesita para renderizar.",
                    "Marca iframes y scripts de terceros que puedan quedar parciales en sandbox.",
                    "Aclara si hay macros o placeholders que dependen de un entorno propietario.",
                ],
            },
            {
                "title": "Audio, autoplay y comportamiento bloqueante",
                "paragraphs": [
                    "Autoplay con sonido, navegacion fuera del frame o comportamiento invasivo suelen convertirse rapido en rechazo tecnico o en una pieza bloqueada.",
                    "Esa capa conviene revisarla antes de hablar de polish visual porque afecta aprobacion, experiencia de usuario y compatibilidad con el contexto de serving.",
                ],
                "bullets": [
                    "Detecta autoplay con sonido o audio al cargar.",
                    "Comprueba que la pieza no intente escapar del frame.",
                    "Documenta cualquier comportamiento que dependa de interaccion del usuario.",
                ],
            },
            {
                "title": "Preview y QA no son lo mismo",
                "paragraphs": [
                    "El preview sirve para responder si el markup renderiza de forma legible dentro de un contenedor controlado. El QA sirve para decidir si la pieza cumple criterios tecnicos y si esta lista para pasar al siguiente paso.",
                    "En una revision inicial suelen convivir ambos: primero usas preview para ver el comportamiento visible y despues checklist para decidir si hay alertas o bloqueos reales.",
                ],
            },
            {
                "title": "Limitaciones de una revision inicial",
                "paragraphs": [
                    "Una revision inicial no replica SafeFrame, requests de red, clics reales ni el comportamiento final de un ad server. Su valor esta en acotar problemas y separar lo evidente de lo que todavia requiere entorno real.",
                    "Eso significa que una creatividad puede verse correcta en preview y aun asi necesitar QA adicional, igual que puede quedar parcial en sandbox y seguir siendo valida dentro de un entorno propietario.",
                ],
            },
        ],
        "related_tool_slugs": ["creative-preview-lab", "creative-qa-checklist"],
        "related_seo_page_slugs": ["validar-creatividad-html", "preview-anuncios-html", "como-validar-tags-publicitarios"],
        "related_knowledge_slugs": [
            "errores-comunes-en-implementaciones-con-google-publisher-tag",
            "como-crear-urls-con-parametros-utm-correctamente",
        ],
        "faqs": [
            {
                "question": "Que conviene revisar primero en una creatividad HTML?",
                "answer": "Dimensiones, peso, click path y dependencias externas. Esa base suele explicar buena parte de los fallos que despues aparecen en serving o QA final.",
            },
            {
                "question": "Preview y QA tecnico publicitario son lo mismo?",
                "answer": "No. El preview te muestra comportamiento visible del markup. El QA tecnico ordena criterios de aprobacion y separa observaciones de bloqueos reales.",
            },
            {
                "question": "Una revision inicial reemplaza el QA final del ad server?",
                "answer": "No. Sirve para llegar mejor preparado al entorno real, pero no sustituye la validacion final en el contexto donde la pieza va a servir.",
            },
        ],
    },
    {
        "slug": "errores-comunes-en-implementaciones-con-google-publisher-tag",
        "title": "Errores comunes en implementaciones con Google Publisher Tag | Pi Development",
        "meta_description": "Guia tecnica sobre errores comunes en implementaciones con Google Publisher Tag: carga de GPT, slots, refresh, stack parcial y diferencias entre backend y navegador.",
        "meta_keywords": "google publisher tag, errores gpt, debug ads, diagnostico tecnico publicitario, herramientas para google publisher tag",
        "eyebrow": "AdTech",
        "cluster_key": "adtech",
        "h1": "Errores comunes en implementaciones con Google Publisher Tag",
        "description": "Muchos problemas atribuidos a Google Publisher Tag en realidad mezclan errores de carga, slots poco claros, refresh mal resuelto o lecturas incompletas del stack publicitario.",
        "summary": "Guia para detectar errores frecuentes en implementaciones con GPT y distinguir lo que puede leerse desde backend de lo que todavia requiere navegador.",
        "intro_paragraphs": [
            "Cuando una pagina monetizada falla, Google Publisher Tag suele quedar en el centro del diagnostico aunque el problema no siempre este en la libreria misma. A veces la carga es parcial, a veces los slots no son legibles y a veces el stack completo solo aparece en runtime.",
            "Por eso conviene ordenar primero los errores mas comunes: carga visible de GPT, definicion de slots, logica de refresh y alcance real del analisis que haces desde backend frente a lo que solo vas a confirmar en navegador.",
        ],
        "sections": [
            {
                "title": "Errores de carga y presencia parcial de GPT",
                "paragraphs": [
                    "Lo primero es confirmar si la pagina expone senales compatibles con gpt.js o googletag en la respuesta inicial. Si esa base ni siquiera aparece, el problema no esta en el refresh ni en el inventario, sino en la carga visible del stack.",
                    "Tambien conviene documentar cuando la libreria parece presente pero el resto del stack queda difuso. Esa combinacion ya es una pista util antes de pasar a una inspeccion mas profunda.",
                ],
                "bullets": [
                    "GPT no visible en el HTML inicial.",
                    "Libreria visible, pero sin evidencia clara de slots o contenedores.",
                    "Carga mezclada con wrappers o vendors que vuelven opaco el diagnostico.",
                ],
            },
            {
                "title": "Slots mal definidos o dificiles de rastrear",
                "paragraphs": [
                    "Una implementacion puede cargar GPT y aun asi dejar una estructura de slots muy poco legible. Eso complica el debug porque no queda claro donde empieza el problema: inventario, naming de slots o contenedores montados del lado del cliente.",
                    "El objetivo de la primera pasada no es reconstruir todo el runtime, sino confirmar si el HTML inicial ya deja pistas suficientes sobre contenedores, iframes o placements.",
                ],
                "bullets": [
                    "Contenedores sin naming claro o dificiles de mapear.",
                    "Hints de slots inconsistentes con la estructura visible.",
                    "Iframes publicitarios visibles sin una relacion clara con el slot esperado.",
                ],
            },
            {
                "title": "Problemas de refresh y decisiones que dependen del runtime",
                "paragraphs": [
                    "El refresh suele discutirse como si fuera un detalle menor, pero puede estar ligado a triggers del navegador, lazy load, visibilidad de slots o logica de wrappers.",
                    "Desde backend puedes detectar algunas pistas, pero no conviene presentar esa lectura como si confirmara comportamiento real en runtime. El valor esta en dejar claro cuando el stack visible no alcanza para cerrar el diagnostico.",
                ],
            },
            {
                "title": "Backend y navegador no responden la misma pregunta",
                "paragraphs": [
                    "El analisis backend sirve para detectar senales visibles, vendors, scripts, iframes y stack parcial en la respuesta inicial. El navegador sirve para validar ejecucion, requests, callbacks y comportamiento real de carga.",
                    "Confundir ambas capas lleva a conclusiones pobres: o se sobreinterpreta una lectura backend o se entra al navegador sin una hipotesis clara sobre que buscar.",
                ],
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
                "question": "Una lectura backend alcanza para debuggear Google Publisher Tag?",
                "answer": "No por si sola. Sirve para detectar senales visibles y ordenar hipotesis, pero el comportamiento real de carga y refresh sigue necesitando navegador.",
            },
            {
                "question": "Que error se repite mas en implementaciones con GPT?",
                "answer": "Es frecuente ver GPT visible sin una estructura clara de slots, o una mezcla de wrappers y vendors que vuelve opaca la lectura del inventario.",
            },
            {
                "question": "Cuando conviene sumar AI Auditor a un debug de GPT?",
                "answer": "Cuando quieres cruzar la capa publicitaria con el estado tecnico general de la URL y confirmar si la pagina tiene otros problemas visibles que agravan el contexto.",
            },
        ],
    },
    {
        "slug": "como-crear-urls-con-parametros-utm-correctamente",
        "title": "Cómo crear URLs con parámetros UTM correctamente | Pi Development",
        "meta_description": "Guia tecnica para crear URLs con parametros UTM correctamente: que son, para que sirven, errores comunes, naming limpio y ejemplos practicos.",
        "meta_keywords": "como crear urls con parametros utm, parametros utm, utm builder, tracking utm",
        "eyebrow": "Tracking",
        "cluster_key": "tracking",
        "h1": "Cómo crear URLs con parámetros UTM correctamente",
        "description": "Las UTMs parecen simples, pero varios errores de tracking empiezan antes de analytics: naming inconsistente, sobrescritura de queries, URLs rotas o parametros agregados sin criterio.",
        "summary": "Guia tecnica para construir URLs con UTMs limpias, preservar la URL base y evitar errores operativos antes de compartir una campana.",
        "intro_paragraphs": [
            "Los parametros UTM sirven para identificar fuente, medio, campana y otros detalles de una URL que va a circular en medios, email, paid social u otros canales operativos.",
            "El problema es que muchas veces se agregan a mano, sin preservar query params existentes y sin una conviccion minima de naming. El resultado es una URL poco legible, dificil de comparar y facil de romper.",
        ],
        "sections": [
            {
                "title": "Que son las UTMs y para que sirven",
                "paragraphs": [
                    "Las UTMs son parametros que se agregan a una URL para identificar de donde viene el trafico y bajo que criterio operativo fue compartida esa direccion.",
                    "No son una capa de SEO ni una solucion magica de analitica. Su utilidad esta en dejar mas claro el origen de la visita y en sostener una lectura consistente entre equipos.",
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
                    "Los errores mas frecuentes no son complejos: repetir claves, sobrescribir parametros que ya estaban en la URL, inventar nomenclaturas nuevas en cada campana o compartir una URL final que nadie reviso completa.",
                    "Tambien es habitual usar nombres demasiado largos o poco consistentes, lo que vuelve mas dificil comparar resultados despues.",
                ],
                "bullets": [
                    "Romper query params existentes al pegar UTMs a mano.",
                    "Usar source, medium o campaign con naming distinto para el mismo caso.",
                    "Agregar parametros opcionales sin una razon clara.",
                    "No comprobar la URL final completa antes de compartirla.",
                ],
            },
            {
                "title": "Naming limpio y legible",
                "paragraphs": [
                    "Un naming limpio no significa burocracia. Significa que alguien mas del equipo pueda leer la URL final y entender con bastante rapidez de que canal y campana se trata.",
                    "Si cada persona inventa una convencion nueva, las UTMs dejan de ser una ayuda operativa y se convierten en ruido.",
                ],
                "bullets": [
                    "Mantener source y medium en minusculas y sin espacios.",
                    "Usar campaign con criterio estable entre acciones comparables.",
                    "Evitar palabras vagas o internas que despues nadie entiende fuera del contexto inmediato.",
                ],
            },
            {
                "title": "Ejemplos practicos",
                "paragraphs": [
                    "Una URL como https://example.com/landing puede pasar a https://example.com/landing?utm_source=newsletter&utm_medium=email&utm_campaign=lanzamiento-q2 si la accion es un envio editorial.",
                    "Si la URL base ya trae parametros funcionales, por ejemplo ref=home, conviene preservarlos y agregar las UTMs sin destruir esa parte de la direccion.",
                ],
            },
        ],
        "related_tool_slugs": ["utm-builder"],
        "related_seo_page_slugs": ["como-crear-utms", "analizar-seo-pagina", "herramientas-adtech"],
        "related_knowledge_slugs": [
            "como-validar-una-creatividad-html-antes-de-publicarla",
            "errores-comunes-en-implementaciones-con-google-publisher-tag",
        ],
        "faqs": [
            {
                "question": "Conviene escribir URLs con UTM a mano?",
                "answer": "Solo si el caso es muy simple y aun asi revisas la URL final completa. En flujos reales conviene un builder que preserve parametros y reduzca errores manuales.",
            },
            {
                "question": "UTM Builder reemplaza una convencion de naming?",
                "answer": "No. Ayuda a construir la URL con mas consistencia, pero el criterio de naming sigue dependiendo del equipo y del uso que le van a dar a esos parametros.",
            },
            {
                "question": "Las UTMs afectan la landing que recibe trafico?",
                "answer": "Pueden afectar la URL operativa y la forma en que circula la pagina, por eso tiene sentido revisar tanto el etiquetado como la calidad tecnica de la landing final cuando hace falta.",
            },
        ],
    },
]


def get_knowledge_index_page():
    return deepcopy(KNOWLEDGE_INDEX_PAGE)


def get_knowledge_page(slug):
    for page in KNOWLEDGE_PAGE_DEFINITIONS:
        if page["slug"] == slug:
            return deepcopy(page)
    return None


def get_public_knowledge_slugs():
    return [page["slug"] for page in KNOWLEDGE_PAGE_DEFINITIONS]


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
        if pages:
            groups.append({"cluster_key": cluster_key, "pages": pages})
    return groups
