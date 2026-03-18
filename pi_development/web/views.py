from django.http import Http404, HttpResponse
from django.shortcuts import render


SERVICE_PAGES = {
    "web-development": {
        "eyebrow": "Servicio",
        "title": "Desarrollo web a medida",
        "description": "Sitios y experiencias digitales pensadas para crecer, posicionar y convertir sin depender de una plantilla genérica.",
        "intro": "Diseñamos y desarrollamos sitios con una base clara: velocidad, estructura, contenido y evolución real del negocio.",
        "highlights": [
            "Landings, webs corporativas y bases escalables para futuros productos.",
            "Arquitectura pensada para SEO, rendimiento y mantenimiento simple.",
            "Implementación alineada con marca, objetivos y conversión.",
        ],
        "deliverables_title": "Qué incluye este servicio",
        "deliverables": [
            "Estructura de páginas y navegación lista para crecer.",
            "Diseño visual y desarrollo adaptado al objetivo del negocio.",
            "Base técnica pensada para SEO, performance y futuras campañas.",
        ],
        "for_title": "Ideal para",
        "for_items": [
            "Marcas que hoy tienen una landing limitada y necesitan escalar.",
            "Negocios que quieren separar servicios, casos y contenidos.",
            "Proyectos que buscan una base seria antes de invertir en medios.",
        ],
        "faq": [
            {
                "question": "¿Sirve para una web simple?",
                "answer": "Sí. La idea no es sobredimensionar, sino dejar una base limpia que después pueda crecer sin rehacerse entera.",
            },
            {
                "question": "¿Se puede empezar por una sola página?",
                "answer": "Sí, pero estructurada de forma que luego conviva con servicios, blog, portfolio y nuevas secciones.",
            },
        ],
        "cta_title": "¿Necesitás una web lista para crecer?",
        "cta_text": "Podemos transformar la home actual en una estructura más sólida y lista para campañas, contenido y posicionamiento.",
    },
    "ux-ui": {
        "eyebrow": "Servicio",
        "title": "Diseño UX/UI estratégico",
        "description": "Interfaces claras, consistentes y orientadas a la conversión, no solo a lo visual.",
        "intro": "El objetivo no es decorar pantallas sino construir una experiencia comprensible, usable y alineada con tu propuesta.",
        "highlights": [
            "Jerarquía visual y recorridos más claros para cada tipo de usuario.",
            "Sistemas de componentes que reducen improvisación al crecer el sitio.",
            "Diseño que sostiene branding, lectura y acciones clave.",
        ],
        "deliverables_title": "Qué ordena este servicio",
        "deliverables": [
            "Jerarquías visuales más claras para home, servicios y contenidos.",
            "Patrones reutilizables para que el sitio no se desarme al crecer.",
            "Diseño orientado a lectura, foco y conversión.",
        ],
        "for_title": "Ideal para",
        "for_items": [
            "Sitios con secciones fuertes pero experiencia inconsistente.",
            "Marcas que necesitan profesionalizar su interfaz.",
            "Proyectos que quieren escalar contenido sin perder claridad.",
        ],
        "faq": [
            {
                "question": "¿Esto es solo diseño visual?",
                "answer": "No. Incluye estructura, jerarquía, navegación, lectura y relación entre contenido y acción.",
            },
            {
                "question": "¿Convive con SEO?",
                "answer": "Sí. Un mejor UX/UI ayuda a estructurar mejor páginas, recorridos y señales de calidad para usuarios y buscadores.",
            },
        ],
        "cta_title": "¿Querés que la interfaz trabaje a favor de tu negocio?",
        "cta_text": "Podemos ordenar estructura, contenido y diseño para que cada página tenga un propósito claro.",
    },
    "marketing": {
        "eyebrow": "Servicio",
        "title": "Contenido, redes y marketing digital",
        "description": "Mensajes, formatos y recorridos pensados para atraer audiencia y convertir visitas en oportunidades reales.",
        "intro": "Una buena web sola no alcanza. La propuesta necesita narrativa, distribución y puntos de entrada coherentes.",
        "highlights": [
            "Piezas y mensajes conectados con campañas, contenido y marca.",
            "Estructuras listas para medios, anuncios y futuras automatizaciones.",
            "Base editorial para sumar blog, noticias y recursos propios.",
        ],
        "deliverables_title": "Qué habilita este servicio",
        "deliverables": [
            "Narrativa más clara entre home, servicios y contacto.",
            "Base para futuras campañas, medios y piezas publicitarias.",
            "Puente natural hacia blog, novedades y captación editorial.",
        ],
        "for_title": "Ideal para",
        "for_items": [
            "Marcas que quieren atraer tráfico sin depender de una sola fuente.",
            "Proyectos que necesitan unir sitio, redes y campañas.",
            "Negocios que quieren empezar a pensar en medios y publicidad.",
        ],
        "faq": [
            {
                "question": "¿Esto incluye blog?",
                "answer": "Sí, como parte de una estrategia de contenido más amplia. Por eso en esta fase ya dejamos armada la base editorial del sitio.",
            },
            {
                "question": "¿Sirve aunque todavía no haga publicidad?",
                "answer": "Sí. Cuanto mejor esté la base narrativa y estructural antes, mejor va a rendir cualquier pauta futura.",
            },
        ],
        "cta_title": "¿Buscás una base para escalar visibilidad?",
        "cta_text": "Podemos preparar el sitio para contenido, campañas y nuevas páginas con foco en crecimiento.",
    },
    "seo": {
        "eyebrow": "Servicio",
        "title": "Auditorías y posicionamiento SEO",
        "description": "Revisión técnica, estructural y editorial para mejorar visibilidad sin depender solo de publicidad.",
        "intro": "El SEO útil empieza por una base sana: rutas claras, páginas con intención y una estructura que un buscador pueda entender.",
        "highlights": [
            "Arquitectura de páginas preparada para crecer por temas y servicios.",
            "Mejoras técnicas en contenido, enlazado interno y semántica.",
            "Base compatible con futuras entradas de blog y páginas de captación.",
        ],
        "deliverables_title": "Qué revisa este servicio",
        "deliverables": [
            "Rutas, enlazado interno y semántica de páginas clave.",
            "Relación entre contenido, intención de búsqueda y estructura del sitio.",
            "Prioridades concretas para crecer con servicios, blog y portfolio.",
        ],
        "for_title": "Ideal para",
        "for_items": [
            "Sitios que ya se ven bien pero están flojos a nivel estructura.",
            "Marcas que quieren ganar tráfico orgánico con criterio.",
            "Proyectos que necesitan ordenar antes de invertir en pauta.",
        ],
        "faq": [
            {
                "question": "¿SEO es solo escribir artículos?",
                "answer": "No. También depende de rutas, arquitectura, enlazado interno, semántica y claridad de cada página importante.",
            },
            {
                "question": "¿Conviene hacerlo antes del blog?",
                "answer": "Sí. Si la base del sitio está mejor resuelta, el blog nace con más coherencia y mejores señales estructurales.",
            },
        ],
        "cta_title": "¿Querés posicionar con una estructura más sólida?",
        "cta_text": "Podemos seguir con la siguiente etapa: ordenar arquitectura, contenidos y señales SEO del sitio completo.",
    },
}

SERVICES_OVERVIEW = {
    'eyebrow': 'Servicios',
    'title': 'Servicios pensados para pasar de una landing a una presencia digital seria',
    'description': 'Esta página reúne las líneas principales de trabajo de Pi Development y funciona como puerta de entrada real a cada servicio.',
    'intro': 'La home puede seguir siendo una presentación breve, pero la profundidad tiene que vivir en páginas separadas. Por eso esta vista resume la oferta y distribuye el tráfico interno de manera más clara.',
}

SECTION_PAGES = {
    "process": {
        "eyebrow": "Proceso",
        "title": "Cómo trabajamos",
        "description": "Una vista más clara del método detrás de Pi Development para pasar de una landing a un sistema de páginas útil y sostenible.",
        "intro": "Trabajamos con una lógica simple: entender, diseñar, ejecutar y optimizar. La diferencia está en hacerlo con intención y continuidad.",
        "highlights": [
            "Diagnóstico y definición antes de sumar secciones o nuevas páginas.",
            "Diseño y desarrollo conectados con contenido, navegación y SEO.",
            "Mejora continua después de publicar, no solo durante la entrega.",
        ],
        "deliverables_title": "Cómo baja eso a un proyecto real",
        "deliverables": [
            "Priorización técnica y editorial antes de expandir el sitio.",
            "Ejecución por etapas para no rehacer trabajo dos veces.",
            "Base medible para seguir con contenidos, blog y campañas.",
        ],
        "for_title": "Qué ordena este proceso",
        "for_items": [
            "La relación entre diseño, contenido, SEO y negocio.",
            "Las decisiones de navegación y jerarquía del sitio.",
            "El paso de una one-page a una arquitectura más robusta.",
        ],
        "faq": [],
        "cta_title": "¿Querés bajar esta lógica a tu proyecto?",
        "cta_text": "La siguiente iteración puede transformar cada bloque de la home en una página con contexto real y mejor posicionamiento.",
    },
    "resources": {
        "eyebrow": "Recursos",
        "title": "Herramientas, experimentos y formatos",
        "description": "Una base para agrupar recursos, pruebas, formatos publicitarios y utilidades en un espacio con identidad propia.",
        "intro": "Esta sección prepara el terreno para futuros recursos propios: experimentos, auditorías, herramientas y piezas orientadas a medios.",
        "highlights": [
            "Espacio preparado para sumar recursos sin mezclarlos con la landing principal.",
            "Base para futuras páginas, utilidades descargables o piezas de apoyo.",
            "Estructura alineada con una estrategia futura de blog, noticias y monetización.",
        ],
        "deliverables_title": "Qué podría vivir acá más adelante",
        "deliverables": [
            "Herramientas simples de utilidad para marketing, diseño o desarrollo.",
            "Recursos editoriales, plantillas y auditorías descargables.",
            "Formatos especiales para campañas, medios y presencia pública.",
        ],
        "for_title": "Por qué importa esta sección",
        "for_items": [
            "Te permite separar contenidos propios de la home comercial.",
            "Abre una línea natural hacia branding, recursos y comunidad.",
            "Prepara el terreno para monetización y autoridad temática.",
        ],
        "faq": [],
        "cta_title": "¿Querés convertir esta sección en un hub real?",
        "cta_text": "Se puede ampliar después con categorías, fichas de recursos y contenidos indexables.",
    },
}

PORTFOLIO_ITEMS = [
    {
        "name": "Arcade World",
        "category": "Web temática",
        "summary": "Un sitio con fuerte identidad visual y foco en experiencia inmersiva.",
        "image": "web/img/1.png",
    },
    {
        "name": "Blog de Inteligencia Emocional",
        "category": "Contenido y marca personal",
        "summary": "Una base editorial clara para artículos, posicionamiento y lectura guiada.",
        "image": "web/img/2.png",
    },
    {
        "name": "Proyecto editorial",
        "category": "Diseño de contenidos",
        "summary": "Una propuesta visual orientada a lectura, estructura y continuidad temática.",
        "image": "web/img/3.png",
    },
    {
        "name": "Sistem Vesta",
        "category": "Sitio corporativo",
        "summary": "Un caso con foco en claridad, confianza y presentación técnica del servicio.",
        "image": "web/img/4.png",
    },
    {
        "name": "Juno Metales",
        "category": "Negocio industrial",
        "summary": "Una presencia digital pensada para ordenar oferta, marca y contacto comercial.",
        "image": "web/img/5.png",
    },
]

BLOG_PAGE = {
    'eyebrow': 'Blog',
    'title': 'Medios, noticias y contenido estratégico',
    'description': 'La base editorial del sitio para publicar análisis, novedades y contenido que ayude a posicionar, atraer audiencia y preparar futuras campañas.',
    'intro': 'Esta página no es todavía un blog dinámico, pero sí una base editorial real para que el sitio deje de depender solo de la landing y empiece a crecer por temas.',
    'pillars': [
        {
            'title': 'Noticias y novedades',
            'text': 'Una línea para publicaciones más ligadas a actualidad, movimiento del proyecto y presencia pública.',
        },
        {
            'title': 'Guías y análisis',
            'text': 'Contenido que ayude a posicionar búsquedas útiles y construir autoridad temática con más profundidad.',
        },
        {
            'title': 'Opinión y medios',
            'text': 'Un espacio para piezas con mirada propia que luego también se puedan usar en campañas o presencia en redes.',
        },
    ],
    'sample_posts': [
        {
            'category': 'SEO',
            'title': 'Cómo pasar de una one-page a una arquitectura SEO más sólida',
            'summary': 'Un contenido ideal para explicar decisiones estructurales, enlazado interno y crecimiento por servicios.',
        },
        {
            'category': 'Diseño',
            'title': 'Qué cambia cuando una web deja de verse solo linda y empieza a convertir',
            'summary': 'Un enfoque útil para mostrar criterio de UX/UI aplicado a negocio, no solo estética.',
        },
        {
            'category': 'Marketing',
            'title': 'Por qué conviene ordenar contenido antes de invertir en publicidad',
            'summary': 'Una pieza muy alineada con el objetivo futuro de monetización y campañas.',
        },
    ],
}


def _related_service_pages(current_slug):
    links = [
        {
            'title': page['title'],
            'description': page['description'],
            'url': f"/services/{slug}/",
        }
        for slug, page in SERVICE_PAGES.items()
        if slug != current_slug
    ]
    links.append(
        {
            'title': 'Servicios',
            'description': SERVICES_OVERVIEW['description'],
            'url': '/services/',
        }
    )
    return links


def _related_section_pages(current_slug):
    links = [
        {
            'title': page['title'],
            'description': page['description'],
            'url': f"/{slug}/" if slug in {'process', 'resources'} else '/',
        }
        for slug, page in SECTION_PAGES.items()
        if slug != current_slug
    ]
    links.extend([
        {
            'title': 'Portfolio',
            'description': 'Casos y trabajos que muestran la propuesta en piezas concretas.',
            'url': '/portfolio/',
        },
        {
            'title': 'Blog',
            'description': BLOG_PAGE['description'],
            'url': '/blog/',
        },
    ])
    return links


def index(request):
    return render(request, 'web/index.html', {'portfolio_items': PORTFOLIO_ITEMS})


def services(request):
    service_cards = []
    for slug, page in SERVICE_PAGES.items():
        service_cards.append({
            'slug': slug,
            'title': page['title'],
            'description': page['description'],
        })
    context = {
        'overview': SERVICES_OVERVIEW,
        'service_cards': service_cards,
    }
    return render(request, 'web/services_page.html', context)


def about(request):
    return render(request, 'web/about_page.html')


def contact(request):
    return render(request, 'web/contact_page.html')


def policies(request):
    return render(request, 'web/policies.html')


def portfolio(request):
    return render(request, 'web/portfolio_page.html', {'portfolio_items': PORTFOLIO_ITEMS})


def blog(request):
    return render(request, 'web/blog_page.html', {'blog_page': BLOG_PAGE})


def content_page(request, section, slug):
    if section == 'services':
        page = SERVICE_PAGES.get(slug)
        page_type = 'service'
        related_pages = _related_service_pages(slug)
    elif section == 'sections':
        page = SECTION_PAGES.get(slug)
        page_type = 'section'
        related_pages = _related_section_pages(slug)
    else:
        page = None
        page_type = 'page'
        related_pages = []

    if page is None:
        raise Http404('Page not found.')

    context = {
        'page': page,
        'page_type': page_type,
        'slug': slug,
        'related_pages': related_pages,
    }
    return render(request, 'web/content_page.html', context)


def robots_txt(request):
    content = [
        'User-Agent: *',
        'Allow: /',
        'Sitemap: https://pidevelopment.web.app/sitemap.xml',
    ]
    return HttpResponse('\n'.join(content), content_type='text/plain')
