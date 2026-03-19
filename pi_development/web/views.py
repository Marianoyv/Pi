from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    AdTechDebugForm,
    AiAuditorForm,
    CreativePreviewLabForm,
    CreativeQAChecklistForm,
    LandingPerformanceSnapshotForm,
    UTMBuilderForm,
)
from .knowledge_pages import (
    get_knowledge_index_page,
    get_knowledge_listing_groups,
    get_knowledge_page,
    get_public_knowledge_slugs,
    get_related_knowledge_pages,
)
from .schema_utils import build_faq_schema_json, build_item_list_schema_json
from .services.tools.creative_preview_lab import run_creative_preview_lab
from .services.tools.creative_qa import run_creative_qa
from .services.tools.adtech_debug import run_adtech_debug
from .services.tools.ai_auditor import run_ai_auditor
from .services.tools.landing_snapshot import run_landing_performance_snapshot
from .services.tools.utm_builder import run_utm_builder
from .seo_pages import get_related_seo_pages, get_seo_page
from .tool_examples import get_tool_example
from .topic_clusters import (
    get_related_seo_pages_for_tool,
    get_topic_cluster_context_for_seo_page,
    get_topic_cluster_context_for_tool,
    get_topic_clusters_for_keys,
    get_topic_clusters_with_content,
)
from .tool_catalog import (
    get_featured_tool,
    get_related_tools,
    get_tool,
    get_tool_groups,
    get_tools,
    get_tools_index_page,
)


WORK_ITEMS = [
    {
        "slug": "arcade-world",
        "name": "Arcade World",
        "category": "Plataforma de experiencia",
        "summary": "Un sistema visual para catálogo, exploración temática y presencia digital con una interfaz intensa pero controlada.",
        "context": "Proyecto de entretenimiento con identidad fuerte y necesidad de ordenar contenido sin perder atmósfera.",
        "problem": "La experiencia necesitaba impacto visual sin sacrificar claridad, carga rápida ni continuidad de navegación.",
        "solution": "Se construyó una arquitectura modular con jerarquía clara, capas visuales contenidas y puntos de entrada consistentes.",
        "implementation": "Frontend a medida, composición de secciones, recursos optimizados y una base lista para sumar nuevas capas.",
        "result": "Una plataforma inmersiva pero legible, preparada para crecer en catálogo y complejidad sin perder control.",
        "highlights": ["Arquitectura visual", "Jerarquía de contenido", "Rendimiento frontend"],
        "image": "web/img/arcade.mp4",
        "media_type": "video",
        "poster": "web/img/1.png",
        "url": "https://arcade-world.web.app/",
    },
    {
        "slug": "blog-int-emocional",
        "name": "Blog Int Emocional",
        "category": "Sistema editorial",
        "summary": "Una base editorial pensada para publicar, posicionar y sostener lectura con estructura en lugar de diseños genéricos.",
        "context": "Proyecto orientado a contenido y marca personal con necesidad de orden, legibilidad y continuidad.",
        "problem": "Hacía falta una plataforma editorial que organizara artículos, jerarquía y narrativa sin sobrecargar la interfaz.",
        "solution": "Se diseñó un sistema de contenido con foco en lectura, semántica, SEO en página y crecimiento por temas.",
        "implementation": "Estructura de páginas, bloques editoriales, navegación simple y base lista para escalar en volumen.",
        "result": "Una capa editorial más sólida y mantenible, preparada para sostener autoridad de contenido con menos fricción.",
        "highlights": ["Base editorial", "SEO en página", "Lectura sostenida"],
        "image": "web/img/2.png",
        "url": "https://blogintemocional.web.app/index.html",
    },
    {
        "slug": "indices-argentinos",
        "name": "Índices Argentinos",
        "category": "Interfaz de datos",
        "summary": "Una interfaz de datos para consultar indicadores con lectura rápida, foco en orden y menor fricción operativa.",
        "context": "Proyecto enfocado en datos económicos con necesidad de claridad, actualización rápida y lectura técnica.",
        "problem": "Los indicadores debían verse de forma útil y sobria, sin ruido visual ni capas decorativas innecesarias.",
        "solution": "Se planteó una interfaz de consulta con jerarquía fuerte, lectura inmediata y estructura preparada para crecer.",
        "implementation": "Sistema visual para tablas, métricas y bloques de consulta priorizando velocidad y claridad.",
        "result": "Una experiencia más técnica y confiable para explorar datos sin depender de interfaces recargadas.",
        "highlights": ["Lectura de datos", "Jerarquía fuerte", "Base escalable"],
        "image": "web/img/indices.png",
        "url": "https://indices-argentinos.web.app/",
    },
    {
        "slug": "recetas-del-sapi",
        "name": "Recetas del Sapi",
        "category": "Plataforma de contenido",
        "summary": "Una estructura de contenido pensada para descubrimiento, navegación y continuidad editorial sin perder cercanía.",
        "context": "Proyecto gastronómico que necesitaba ordenar piezas de contenido y recorrido de lectura.",
        "problem": "El contenido debía sentirse útil y accesible sin caer en una interfaz frágil o desordenada.",
        "solution": "Se trabajó una plataforma editorial clara con foco en categorías, legibilidad y continuidad de exploración.",
        "implementation": "Composición de entradas, módulos de contenido y estructura lista para publicar con criterio.",
        "result": "Un sistema de contenido más estable, fácil de sostener y preparado para seguir creciendo.",
        "highlights": ["Sistema de contenido", "Categorías claras", "Continuidad editorial"],
        "image": "web/img/recetas.png",
        "url": "https://recetasdelsapi.web.app/",
    },
    {
        "slug": "juno-metales",
        "name": "Juno Metales",
        "category": "Plataforma industrial",
        "summary": "Una plataforma corporativa para ordenar oferta, credibilidad y entrada comercial en un contexto industrial.",
        "context": "Negocio industrial con necesidad de presentar servicios y estructura comercial con más claridad.",
        "problem": "La presencia digital debía verse técnica, confiable y simple de recorrer para contactos B2B.",
        "solution": "Se construyó una base corporativa con narrativa sobria, jerarquía clara y puntos de contacto directos.",
        "implementation": "Arquitectura de información, contenidos orientados a negocio y capas de conversión livianas.",
        "result": "Una presencia más seria y operativa para respaldar actividad comercial sin recursos superfluos.",
        "highlights": ["Narrativa B2B", "Jerarquía comercial", "Base industrial"],
        "image": "web/img/juno.mp4",
        "media_type": "video",
        "poster": "web/img/5.png",
        "url": "https://junometales.com/",
    },
    {
        "slug": "system-vesta",
        "name": "System Vesta",
        "category": "Plataforma de servicios",
        "summary": "Un sistema multipágina con foco en claridad, estructura técnica y lectura confiable de la oferta.",
        "context": "Proyecto de servicios que necesitaba una base digital consistente para explicar oferta y proceso.",
        "problem": "El mensaje debía verse técnico y ordenado, sin sobreexplicación ni bloques genéricos de agencia.",
        "solution": "Se definió una interfaz sobria con arquitectura clara, menos ruido y mejor lectura del sistema.",
        "implementation": "Estructura multipágina, jerarquía de secciones y base lista para profundizar contenido.",
        "result": "Una capa comercial más sólida y creíble para presentar una oferta técnica con mejor control.",
        "highlights": ["Arquitectura multipágina", "Lectura técnica", "Base comercial"],
        "image": "web/img/sistemvesta.mp4",
        "media_type": "video",
        "poster": "web/img/4.png",
        "url": "https://systemvesta.com/",
    },
]

PORTFOLIO_WALL_VARIANTS = {
    "arcade-world-video": {"slug": "arcade-world"},
    "arcade-world-shot-1": {"slug": "arcade-world", "image": "web/img/arcade1.png"},
    "arcade-world-shot-2": {"slug": "arcade-world", "image": "web/img/arcade2.png"},
    "arcade-world-shot-3": {"slug": "arcade-world", "image": "web/img/arcade3.png"},
    "blog-int-emocional-main": {"slug": "blog-int-emocional"},
    "blog-int-emocional-shot-1": {"slug": "blog-int-emocional", "image": "web/img/blogie1.png"},
    "blog-int-emocional-shot-2": {"slug": "blog-int-emocional", "image": "web/img/blogie2.png"},
    "indices-argentinos-main": {"slug": "indices-argentinos"},
    "indices-argentinos-shot-1": {"slug": "indices-argentinos", "image": "web/img/indice1.png"},
    "indices-argentinos-shot-2": {"slug": "indices-argentinos", "image": "web/img/indice2.png"},
    "indices-argentinos-shot-3": {"slug": "indices-argentinos", "image": "web/img/indice3.png"},
    "recetas-del-sapi-main": {"slug": "recetas-del-sapi"},
    "juno-metales-video": {"slug": "juno-metales"},
    "system-vesta-video": {"slug": "system-vesta"},
    "system-vesta-shot-1": {"slug": "system-vesta", "image": "web/img/sistemvesta1.png"},
}

PORTFOLIO_WALL_SEQUENCE = [
    "arcade-world-shot-1",
    "blog-int-emocional-shot-2",
    "indices-argentinos-shot-1",
    "recetas-del-sapi-main",
    "system-vesta-shot-1",
    "indices-argentinos-shot-2",
    "arcade-world-shot-2",
    "blog-int-emocional-shot-1",
    "indices-argentinos-main",
    "recetas-del-sapi-main",
    "blog-int-emocional-main",
    "arcade-world-shot-3",
    "indices-argentinos-shot-3",
    "juno-metales-video",
    "recetas-del-sapi-main",
    "blog-int-emocional-shot-2",
    "indices-argentinos-shot-1",
    "system-vesta-shot-1",
    "recetas-del-sapi-main",
    "blog-int-emocional-shot-1",
    "indices-argentinos-shot-2",
    "arcade-world-video",
    "recetas-del-sapi-main",
    "indices-argentinos-main",
    "system-vesta-video",
]

PORTFOLIO_WALL_ECHO_SEQUENCE = [
    "indices-argentinos-shot-1",
    "blog-int-emocional-shot-1",
    "arcade-world-shot-2",
    "recetas-del-sapi-main",
    "system-vesta-shot-1",
    "arcade-world-shot-1",
    "blog-int-emocional-main",
    "indices-argentinos-shot-3",
    "system-vesta-shot-1",
    "recetas-del-sapi-main",
]


def _build_portfolio_wall_items(sequence=None):
    items_by_slug = {item["slug"]: item for item in WORK_ITEMS}
    wall_items = []
    for key in sequence or PORTFOLIO_WALL_SEQUENCE:
        variant = PORTFOLIO_WALL_VARIANTS.get(key)
        if not variant:
            continue
        base_item = items_by_slug.get(variant["slug"])
        if not base_item:
            continue

        wall_item = dict(base_item)
        if variant.get("image"):
            wall_item["image"] = variant["image"]
            wall_item.pop("media_type", None)
            wall_item.pop("poster", None)
        wall_items.append(wall_item)
    return wall_items

HOME_PAGE = {
    "hero": {
        "eyebrow": "Herramientas técnicas para AdTech, creatividades y rendimiento web",
        "title": "Analiza. Valida. Optimiza.",
        "description": "Pi Development reúne herramientas para diagnóstico técnico web, revisión AdTech, validación de creatividades, etiquetado UTM y automatización operativa.",
        "signals": [
            {
                "label": "AdTech",
                "text": "Diagnóstico inicial de GPT, Prebid, slots y señales visibles de monetización.",
                "href": "/herramientas-adtech/",
            },
            {
                "label": "Creatividades",
                "text": "Checklist técnico y vista previa para HTML, rich media y tags publicitarios.",
                "href": "/tools/#qa_preview",
            },
            {
                "label": "Rendimiento web",
                "text": "Revisión rápida de URLs, metadatos, estructura HTML y tiempos de respuesta.",
                "href": "/tools/#diagnostics",
            },
            {
                "label": "Operación",
                "text": "Etiquetado UTM y utilidades para reducir errores manuales en flujos reales.",
                "href": "/tools/#operations",
            },
        ],
    },
    "systems": {
        "eyebrow": "Arquitectura digital",
        "title": "Detrás de cada herramienta hay una arquitectura que la sostiene.",
        "description": "Pi Development no trabaja como agencia. Diseña estructuras digitales para que contenido, datos, automatización y herramientas convivan con criterio técnico.",
        "support_label": "Qué significa aquí",
        "support_text": "La arquitectura digital ordena rutas, módulos, formularios, eventos, datos y automatizaciones para que la capa visible no dependa de parches.",
        "groups": [
            {
                "label": "Base web",
                "title": "Plataformas web",
                "text": "Sistemas de páginas y módulos pensados para contenido, producto o captación sin rehacer la estructura en cada iteración.",
                "outcome": "Más claridad estructural y mejor capacidad para crecer sin deuda innecesaria.",
            },
            {
                "label": "Datos y señal",
                "title": "Tracking y lectura técnica",
                "text": "Capas de medición, reporting y validación para que la operación dependa menos de supuestos.",
                "outcome": "Mejor lectura del sistema y decisiones con señal real.",
            },
            {
                "label": "Automatización",
                "title": "Conexiones y flujos",
                "text": "Integraciones ligeras y automatizaciones para reducir trabajo manual y errores repetitivos.",
                "outcome": "Procesos más limpios y menos fricción operativa.",
            },
            {
                "label": "Producto técnico",
                "title": "Herramientas útiles",
                "text": "Utilidades concretas para revisar, validar o acelerar tareas técnicas con una interfaz sobria.",
                "outcome": "Capacidad visible y funcional, no solo discurso.",
            },
        ],
    },
    "approach": {
        "eyebrow": "Método",
        "title": "Diagnóstico, estructura, desarrollo y mejora continua.",
        "description": "El trabajo parte del problema técnico real y termina en una herramienta o sistema que se pueda usar, mantener y ampliar.",
        "steps": [
            {"number": "01", "title": "Diagnóstico", "text": "Se ordena el contexto, las restricciones y la fricción real antes de decidir qué conviene construir."},
            {"number": "02", "title": "Diseño estructural", "text": "Se define arquitectura, jerarquía, entradas, salidas y límites de la solución."},
            {"number": "03", "title": "Desarrollo", "text": "Se implementa con foco en claridad, mantenimiento simple y utilidad inmediata."},
            {"number": "04", "title": "Optimización", "text": "Se corrige lo que afecta rendimiento, QA, monetización, datos o estabilidad operativa."},
        ],
        "note": "El objetivo no es sumar entregables. Es dejar una base técnica que siga siendo útil cuando el proyecto crece.",
    },
    "tools": {
        "eyebrow": "Herramientas",
        "title": "El foco principal del sitio está aquí.",
        "description": "La suite resuelve tareas concretas: auditar URLs, detectar señales AdTech, validar creatividades, generar URLs con UTM y probar código HTML en un sandbox controlado.",
        "support_title": "Herramientas para uso real",
        "support_text": "Cada herramienta responde a una tarea técnica concreta y está pensada para uso real, no para decorar el catálogo.",
        "groups": [
            {"label": "Diagnóstico web", "title": "Revisión de URLs y landing pages", "text": "Auditoría técnica breve para estado HTTP, metadatos, estructura HTML y oportunidades de mejora."},
            {"label": "AdTech", "title": "Lectura de monetización visible", "text": "Detección inicial de GPT, Google Ad Manager, Prebid, wrappers, slots e iframes publicitarios."},
            {"label": "Creatividades", "title": "QA técnico y vista previa", "text": "Validación de dimensiones, click path, tracking, autoplay, macros y markup dentro de una revisión controlada."},
            {"label": "Operación", "title": "Etiquetado y control", "text": "Construcción de URLs con UTM y otras utilidades para reducir errores manuales."},
        ],
    },
    "portfolio": {
        "eyebrow": "Casos",
        "title": "Sistemas publicados con decisiones técnicas visibles.",
        "description": "No es una galería de maquetas. Son implementaciones reales con contexto, problema, solución y resultado.",
    },
    "about": {
        "eyebrow": "Estudio",
        "title": "Pi Development diseña herramientas y sistemas digitales.",
        "description": "Es un estudio independiente orientado a AdTech, rendimiento web, QA de creatividades, automatización y datos.",
        "support": "La prioridad es construir capas técnicas útiles para detectar problemas, validar implementaciones y ordenar flujos sin ruido innecesario.",
        "values": [
            {"title": "Criterio técnico", "text": "Cada decisión tiene una razón funcional, no solo visual."},
            {"title": "Claridad", "text": "El producto debe entenderse rápido, tanto en la interfaz como en el resultado que devuelve."},
            {"title": "Escalabilidad", "text": "La base se prepara para crecer sin obligar a rehacer todo en cada cambio."},
            {"title": "Sobriedad", "text": "Sin ruido de agencia, sin frases vacías y sin capas decorativas innecesarias."},
        ],
    },
}

SYSTEMS_PAGE = {
    "eyebrow": "Arquitectura digital",
    "title": "Sistemas digitales para operar con más claridad y menos fricción.",
    "description": "Pi Development diseña plataformas, herramientas y capas técnicas para proyectos que necesitan una estructura digital más útil, estable y escalable.",
    "intro_title": "La arquitectura empieza antes de la interfaz.",
    "intro": "Un sistema digital no es solo una página visible. También incluye rutas, formularios, módulos, automatizaciones, datos, eventos y relaciones entre piezas que deben funcionar juntas sin generar deuda técnica.",
    "support_title": "Cuándo conviene pensar en sistema",
    "support_text": "Cuando la capa digital ya sostiene contenido, captación, operación, monetización o validaciones técnicas. En ese punto la estructura importa más que la apariencia aislada.",
    "categories": [
        {
            "label": "Plataformas",
            "title": "Plataformas web",
            "description": "Sistemas preparados para producto, contenido, captación y operación sin rehacer la base cada vez que cambia el alcance.",
            "solves": "Centraliza experiencia, contenido, conversión y flujos de negocio en una sola estructura coherente.",
            "focus": "Arquitectura modular, navegación clara, componentes reutilizables y criterio de rendimiento.",
            "result": "Una base escalable para publicar, operar y evolucionar con más control.",
        },
        {
            "label": "Herramientas",
            "title": "Herramientas técnicas",
            "description": "Utilidades internas o públicas para reducir fricción, automatizar tareas y estandarizar decisiones operativas.",
            "solves": "Elimina trabajo manual repetitivo y ordena procesos digitales de baja o media complejidad.",
            "focus": "Utilidad concreta, mantenimiento simple y ejecución rápida con alcance bien definido.",
            "result": "Menos errores operativos y una capa más útil para el día a día.",
        },
        {
            "label": "Infraestructura",
            "title": "Infraestructura digital",
            "description": "Capas de soporte para formularios, eventos, despliegue, automatizaciones ligeras y conexiones entre herramientas.",
            "solves": "Conecta piezas técnicas que suelen quedar sueltas cuando el sistema crece sin arquitectura.",
            "focus": "Confiabilidad, integraciones limpias, observabilidad básica y menos dependencia de parches.",
            "result": "Operación más estable y una base técnica lista para iterar con menos deuda.",
        },
        {
            "label": "AdTech",
            "title": "Rendimiento, datos y monetización",
            "description": "Estructuras para tracking, reporting, capas de ingresos y lectura operativa de rendimiento o medios.",
            "solves": "Une datos, medios y producto sin depender de configuraciones improvisadas o criterios dispersos.",
            "focus": "Señal consistente, integraciones útiles y decisiones guiadas por lectura técnica real.",
            "result": "Más visibilidad sobre el sistema comercial y mejor control sobre la optimización.",
        },
    ],
    "signals_title": "Señales de que ya no alcanza con una web aislada",
    "signals": [
        "La capa digital ya sostiene contenido, conversión, operación o ingresos y necesita orden estructural.",
        "Hay formularios, herramientas o integraciones resueltas con parches y decisiones desconectadas.",
        "Cada nuevo requerimiento obliga a rehacer páginas, bloques o configuraciones desde cero.",
    ],
    "deliverables_title": "Qué suele quedar construido",
    "deliverables": [
        "Arquitectura de páginas, módulos y rutas pensadas como sistema.",
        "Capas técnicas para integraciones, tracking, automatización o rendimiento.",
        "Una base clara para iterar con más velocidad y menos deuda operativa.",
    ],
    "cta_title": "Si el problema es estructural, hay algo que ordenar y construir.",
    "cta_text": "Podemos trabajar sobre una base nueva o reordenar una capa existente que ya quedó corta.",
}

WORK_PAGE = {
    "eyebrow": "Casos",
    "title": "Casos reales con decisiones técnicas visibles.",
    "description": "No es una galería de maquetas. Son sistemas publicados con contexto, restricciones, decisiones técnicas y resultados observables.",
    "notes_title": "Qué mirar en estos casos",
    "notes": [
        "Cómo se ordenó el problema antes de diseñar la solución.",
        "Qué capas estructurales se construyeron para que el sistema pudiera crecer.",
        "Cómo cambia el resultado cuando la arquitectura se piensa con criterio técnico.",
    ],
}

APPROACH_PAGE = {
    "eyebrow": "Método",
    "title": "Un método simple para sistemas que deben durar.",
    "description": "Pi Development trabaja con una secuencia clara: diagnóstico, diseño estructural, desarrollo y optimización. Sin capas innecesarias ni procesos teatrales.",
    "lead": "Cada etapa reduce incertidumbre y deja una base útil para la siguiente. El objetivo no es producir entregables por volumen, sino construir un sistema que siga funcionando cuando crece.",
    "stages": [
        {
            "title": "Diagnóstico",
            "text": "Se mapean contexto, objetivo, restricciones, dependencias y fricción real antes de sumar piezas o funcionalidades.",
        },
        {
            "title": "Diseño estructural",
            "text": "Se define arquitectura, módulos, jerarquía de contenido, datos y recorridos con criterio de sistema.",
        },
        {
            "title": "Desarrollo",
            "text": "Se construye con foco en estabilidad, claridad operativa y mantenimiento simple, no en complejidad innecesaria.",
        },
        {
            "title": "Optimización",
            "text": "Se mide, corrige y mejora lo que afecta rendimiento, lectura, conversión u operación diaria.",
        },
    ],
    "principles": [
        "Sin burocracia innecesaria.",
        "Sin funcionalidades que no respondan a un problema real.",
        "Sin decisiones importantes tomadas sin lectura técnica, datos o contexto.",
    ],
    "fit_title": "Este método encaja mejor cuando",
    "fit_items": [
        "El problema es estructural y no se resuelve con otra capa cosmética.",
        "Hace falta ordenar una base digital que mezcla contenido, operación, herramientas o monetización.",
        "Se necesita una ejecución técnica con criterio, sin separar estrategia y construcción.",
    ],
}

ABOUT_PAGE = {
    "eyebrow": "Estudio",
    "title": "Estudio independiente de herramientas y sistemas digitales.",
    "description": "Pi Development trabaja como estudio técnico para AdTech, validación de creatividades, rendimiento web, automatización y datos.",
    "intro": "El enfoque está en diseñar sistemas útiles, sobrios y técnicamente legibles para equipos que necesitan crecer con estructura.",
    "paragraphs": [
        "La mezcla es deliberada: producto, desarrollo, contenido estructural, rendimiento, automatización, monetización y validación técnica. Cuando esas capas se piensan juntas, el sistema escala mejor y genera menos deuda.",
        "Pi Development trabaja con menos ruido, menos gestos marketineros y más criterio técnico. La prioridad es que cada decisión tenga una razón operativa detrás.",
    ],
    "values": [
        {
            "title": "Pensamiento sistémico",
            "text": "Cada capa se define por su relación con el resto del sistema, no por estética aislada.",
        },
        {
            "title": "Precisión técnica",
            "text": "Arquitectura clara, decisiones trazables y foco en rendimiento real desde la base.",
        },
        {
            "title": "Escalabilidad",
            "text": "Se construye con espacio para crecer, no para quedar rehaciendo la base a los tres meses.",
        },
        {
            "title": "Sobriedad técnica",
            "text": "Menos ruido visual y verbal. Más consistencia, más claridad y mejor lectura del sistema.",
        },
    ],
    "audience_title": "Con quién encaja mejor",
    "audience": [
        "Equipos que necesitan más que una web aislada y quieren una capa digital con estructura.",
        "Proyectos que combinan contenido, operación, automatización, rendimiento o monetización.",
        "Negocios que valoran ejecución técnica, claridad y una base preparada para crecer.",
    ],
}

CONTACT_PAGE = {
    "eyebrow": "Contacto",
    "title": "Cuéntame qué necesitas analizar, validar u optimizar.",
    "description": "Pi Development trabaja sobre herramientas, plataformas y sistemas digitales con foco en AdTech, creatividades, rendimiento web, automatización y datos.",
    "section_title": "Proyectos donde Pi Development aporta más",
    "fit_items": [
        "Plataformas que necesitan una base más clara para crecer.",
        "Herramientas o automatizaciones para resolver fricción operativa real.",
        "Reestructuraciones donde ya existen capas digitales, pero falta criterio de sistema.",
    ],
    "response_note": "Si todavía no está todo definido, basta con explicar el problema, la URL o el contexto actual.",
}

BLOG_PAGE = {
    "eyebrow": "Editorial",
    "title": "La capa editorial llegará cuando tenga estructura real.",
    "description": "El blog queda reservado para análisis técnicos, notas de arquitectura digital y observaciones sobre sistemas, herramientas y rendimiento.",
    "intro_title": "No vamos a publicar por publicar.",
    "intro": "Cuando la capa editorial se abra, va a funcionar como una extensión del sistema de marca: contenido técnico, indexable y útil, no relleno para parecer activos.",
    "groups": [
        {
            "title": "Arquitectura digital",
            "text": "Notas sobre sistemas web, decisiones estructurales y bases técnicas que sostienen crecimiento real.",
        },
        {
            "title": "Rendimiento",
            "text": "Lecturas concretas sobre velocidad, fricción operativa, peso de interfaz y optimización continua.",
        },
        {
            "title": "AdTech y datos",
            "text": "Observaciones sobre medición, capas de ingresos, herramientas operativas y criterios para leer sistemas con datos.",
        },
    ],
    "examples": [
        {
            "category": "Planificado",
            "title": "De one page a sistema digital",
            "summary": "Cómo cambia la arquitectura cuando el sitio deja de ser una presentación y pasa a ser una capa operativa.",
        },
        {
            "category": "Planificado",
            "title": "Rendimiento sin obsesión estética",
            "summary": "Por qué rendimiento, lectura y claridad suelen mejorar cuando el sistema pierde ruido.",
        },
        {
            "category": "Planificado",
            "title": "Herramientas pequeñas, impacto real",
            "summary": "Dónde una utilidad puntual resuelve más que una plataforma sobredimensionada.",
        },
    ],
}

LEGACY_SERVICE_SLUGS = {"web-development", "ux-ui", "marketing", "seo"}
LIVE_TOOL_CONFIG = {
    "ai-auditor": {
        "form_class": AiAuditorForm,
        "service_attr": "run_ai_auditor",
        "template": "web/ai_auditor_page.html",
        "context_key": "audit_result",
        "service_input": "url",
    },
    "adtech-debug-tool": {
        "form_class": AdTechDebugForm,
        "service_attr": "run_adtech_debug",
        "template": "web/adtech_debug_tool_page.html",
        "context_key": "debug_result",
        "service_input": "url",
    },
    "utm-builder": {
        "form_class": UTMBuilderForm,
        "service_attr": "run_utm_builder",
        "template": "web/utm_builder_page.html",
        "context_key": "utm_result",
        "service_input": "cleaned_data",
    },
    "landing-performance-snapshot": {
        "form_class": LandingPerformanceSnapshotForm,
        "service_attr": "run_landing_performance_snapshot",
        "template": "web/landing_snapshot_page.html",
        "context_key": "landing_result",
        "service_input": "url",
    },
    "creative-qa-checklist": {
        "form_class": CreativeQAChecklistForm,
        "service_attr": "run_creative_qa",
        "template": "web/creative_qa_page.html",
        "context_key": "qa_result",
        "service_input": "cleaned_data",
    },
    "creative-preview-lab": {
        "form_class": CreativePreviewLabForm,
        "service_attr": "run_creative_preview_lab",
        "template": "web/creative_preview_lab_page.html",
        "context_key": "preview_result",
        "service_input": "cleaned_data",
    },
}


def index(request):
    return render(
        request,
        "web/index.html",
        {
            "home_page": HOME_PAGE,
            "contact_page": CONTACT_PAGE,
            "portfolio_items": WORK_ITEMS,
            "portfolio_wall_items": _build_portfolio_wall_items(),
            "portfolio_wall_echo_items": _build_portfolio_wall_items(PORTFOLIO_WALL_ECHO_SEQUENCE),
        },
    )


def favicon(request):
    return redirect(staticfiles_storage.url("web/img/pi.ico"), permanent=True)


def systems(request):
    return render(request, "web/systems_page.html", {"systems_page": SYSTEMS_PAGE})


def tools(request):
    tools_page = get_tools_index_page()
    featured_tool = get_featured_tool()
    tools_catalog = get_tools()
    tool_groups = get_tool_groups()
    topic_clusters = get_topic_clusters_with_content()
    structured_data_json = [
        item
        for item in [
            build_item_list_schema_json(
                tools_page["catalog_title"],
                [
                    {
                        "name": tool["name"],
                        "url": request.build_absolute_uri(f"/tools/{tool['slug']}/"),
                    }
                    for tool in tools_catalog
                ],
            )
        ]
        if item
    ]
    return render(
        request,
        "web/tools_page.html",
        {
            "tools_page": tools_page,
            "featured_tool": featured_tool,
            "tools_catalog": tools_catalog,
            "tool_groups": tool_groups,
            "topic_clusters": topic_clusters,
            "structured_data_json": structured_data_json,
        },
    )


def tool_detail(request, slug):
    tool = get_tool(slug)
    if not tool:
        raise Http404("Tool not found.")

    related_tools = get_related_tools(slug)
    related_seo_pages = get_related_seo_pages_for_tool(slug)
    topic_cluster = get_topic_cluster_context_for_tool(slug)
    live_tool_config = LIVE_TOOL_CONFIG.get(tool["slug"])
    if live_tool_config:
        return _render_live_tool(request, tool, related_tools, related_seo_pages, topic_cluster, live_tool_config)

    return render(
        request,
        "web/tool_detail_page.html",
        {
            "tool": tool,
            "related_tools": related_tools,
            "related_seo_pages": related_seo_pages,
            "topic_cluster": topic_cluster,
            "structured_data_json": _build_tool_structured_data(tool),
        },
    )


def work(request):
    return render(
        request,
        "web/work_page.html",
        {
            "work_page": WORK_PAGE,
            "work_items": WORK_ITEMS,
        },
    )


def approach(request):
    return render(request, "web/approach_page.html", {"approach_page": APPROACH_PAGE})


def about(request):
    return render(request, "web/about_page.html", {"about_page": ABOUT_PAGE})


def contact(request):
    return render(request, "web/contact_page.html", {"contact_page": CONTACT_PAGE})


def blog(request):
    knowledge_index_page = get_knowledge_index_page()
    knowledge_groups = _build_knowledge_listing_groups()
    structured_data_json = [
        item
        for item in [
            build_item_list_schema_json(
                knowledge_index_page["title"],
                [
                    {
                        "name": page["h1"],
                        "url": request.build_absolute_uri(reverse("knowledge_page", kwargs={"slug": page["slug"]})),
                    }
                    for group in knowledge_groups
                    for page in group["pages"]
                ],
            )
        ]
        if item
    ]

    return render(
        request,
        "web/blog_page.html",
        {
            "knowledge_index_page": knowledge_index_page,
            "knowledge_groups": knowledge_groups,
            "structured_data_json": structured_data_json,
        },
    )


def knowledge_page(request, slug):
    page = get_knowledge_page(slug)
    if not page:
        raise Http404("Page not found.")

    related_tools = [tool for tool in (get_tool(item) for item in page.get("related_tool_slugs", [])) if tool]
    related_seo_pages = get_related_seo_pages(page.get("related_seo_page_slugs", []))
    related_knowledge_pages = get_related_knowledge_pages(page.get("related_knowledge_slugs", []))
    topic_clusters = get_topic_clusters_for_keys([page["cluster_key"]])
    topic_cluster = topic_clusters[0] if topic_clusters else None
    structured_data_json = [item for item in [build_faq_schema_json(page.get("faqs"))] if item]

    return render(
        request,
        "web/knowledge_article_page.html",
        {
            "knowledge_page": page,
            "related_tools": related_tools,
            "related_seo_pages": related_seo_pages,
            "related_knowledge_pages": related_knowledge_pages,
            "topic_cluster": topic_cluster,
            "structured_data_json": structured_data_json,
        },
    )


def seo_page(request, slug):
    page = get_seo_page(slug)
    if not page:
        raise Http404("Page not found.")

    primary_tool = get_tool(page["primary_tool_slug"])
    related_tools = [tool for tool in (get_tool(item) for item in page.get("related_tool_slugs", [])) if tool]
    related_pages = get_related_seo_pages(page.get("related_page_slugs", []))
    topic_cluster = get_topic_cluster_context_for_seo_page(slug)
    hub_sections = _build_seo_page_hub_sections(page)
    structured_data_json = [item for item in [build_faq_schema_json(page.get("faqs"))] if item]

    return render(
        request,
        "web/seo_landing_page.html",
        {
            "seo_page": page,
            "primary_tool": primary_tool,
            "related_tools": related_tools,
            "related_pages": related_pages,
            "topic_cluster": topic_cluster,
            "hub_sections": hub_sections,
            "hub_use_cases": page.get("hub_use_cases", []),
            "structured_data_json": structured_data_json,
        },
    )


def policies(request):
    return render(request, "web/policies.html")


def legacy_services(request):
    return redirect("systems", permanent=True)


def legacy_service_page(request, slug):
    if slug not in LEGACY_SERVICE_SLUGS:
        raise Http404("Page not found.")
    return redirect("systems", permanent=True)


def legacy_portfolio(request):
    return redirect("work", permanent=True)


def legacy_process(request):
    return redirect("approach", permanent=True)


def legacy_resources(request):
    return redirect("tools", permanent=True)


def robots_txt(request):
    site_url = getattr(settings, "SITE_URL", "").rstrip("/")
    sitemap_url = f"{site_url}{reverse('sitemap')}" if site_url else request.build_absolute_uri(reverse("sitemap"))
    content = [
        "User-Agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(content), content_type="text/plain")


def _render_live_tool(request, tool, related_tools, related_seo_pages, topic_cluster, config):
    tool_example = get_tool_example(tool["slug"])
    example_requested = request.method == "POST" and request.POST.get("_use_example") == "1" and tool_example
    form_payload = tool_example["form_data"] if example_requested else (request.POST or None)
    form = config["form_class"](form_payload)
    result = None
    service = globals()[config["service_attr"]]

    if request.method == "POST" and form.is_valid():
        service_input = config.get("service_input", "url")
        if service_input == "cleaned_data":
            result = service(form.cleaned_data)
        else:
            result = service(form.cleaned_data["url"])

    return render(
        request,
        config["template"],
        {
            "tool": tool,
            "related_tools": related_tools,
            "related_seo_pages": related_seo_pages,
            "topic_cluster": topic_cluster,
            "tool_example": tool_example,
            "tool_example_used": bool(example_requested),
            "structured_data_json": _build_tool_structured_data(tool),
            "form": form,
            config["context_key"]: result,
        },
    )


def _build_tool_structured_data(tool):
    faq_schema = build_faq_schema_json(((tool.get("editorial") or {}).get("faqs") or []))
    return [item for item in [faq_schema] if item]


def _build_seo_page_hub_sections(page):
    section_definitions = page.get("hub_sections", [])
    if not section_definitions:
        return []

    sections = []
    for section in section_definitions:
        cluster = get_topic_clusters_for_keys([section["cluster_key"]], current_seo_slug=page["slug"])
        section_context = dict(section)
        section_context["cluster"] = cluster[0] if cluster else None
        sections.append(section_context)
    return sections


def _build_knowledge_listing_groups():
    groups = []
    for group in get_knowledge_listing_groups():
        clusters = get_topic_clusters_for_keys([group["cluster_key"]])
        group_context = dict(group)
        group_context["cluster"] = clusters[0] if clusters else None
        groups.append(group_context)
    return groups
