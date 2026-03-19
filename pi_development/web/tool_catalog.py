from copy import deepcopy


TOOLS_INDEX_PAGE = {
    "eyebrow": "Herramientas",
    "title": "Herramientas para análisis AdTech, validación de creatividades y diagnóstico técnico web.",
    "description": "La suite de Pi Development reúne utilidades reales para detectar problemas, validar implementaciones y acelerar decisiones técnicas sin ruido visual ni promesas vacías.",
    "seo_title": "Tools de AdTech, creatividades, SEO tecnico y tracking | Pi Development",
    "featured_label": "Herramienta destacada",
    "featured_title": "AI Auditor",
    "featured_description": "Un auditor técnico web para revisar una URL pública y devolver un diagnóstico breve sobre estado general, rendimiento base, SEO y oportunidades concretas.",
    "catalog_title": "Suite técnica lista para uso real",
    "catalog_description": "Cada herramienta resuelve una tarea específica: revisar una landing, detectar señales AdTech, validar creatividades, construir URLs con UTM o probar código HTML dentro de una vista previa controlada.",
    "meta_keywords": "herramientas AdTech, validación de creatividades, diagnóstico técnico web, auditoría SEO básica, generador UTM",
}

TOOL_GROUPS = {
    "diagnostics": {
        "key": "diagnostics",
        "title": "Diagnóstico técnico",
        "description": "Herramientas para analizar URLs, detectar señales técnicas y revisar implementaciones visibles desde backend.",
    },
    "operations": {
        "key": "operations",
        "title": "Operación y etiquetado",
        "description": "Utilidades para construir salidas consistentes, reducir errores manuales y mantener criterios de trabajo más claros.",
    },
    "qa_preview": {
        "key": "qa_preview",
        "title": "QA y vista previa",
        "description": "Herramientas para revisar creatividades, validar criterios básicos y hacer pruebas visuales sin salir de la suite.",
    },
}

DIAGNOSTIC_TOOLS = [
    {
        "slug": "ai-auditor",
        "name": "AI Auditor",
        "tag": "Diagnóstico web",
        "status_label": "Activa",
        "status_tone": "live",
        "summary": "Auditoría técnica breve para una URL pública.",
        "description": "Analiza una URL y devuelve un diagnóstico técnico resumido con estado general, observaciones, rendimiento básico, SEO básico, oportunidades y recomendación.",
        "seo_title": "Auditor técnico web y SEO básico para URLs | Pi Development",
        "meta_description": "AI Auditor revisa una URL pública y entrega un diagnóstico técnico con rendimiento básico, SEO, hallazgos y prioridades de mejora.",
        "meta_keywords": "auditor técnico web, auditoría SEO básica, análisis de URL, diagnóstico técnico web, rendimiento web",
        "page_title": "Auditor técnico web para revisar URLs públicas",
        "page_description": "AI Auditor analiza una URL desde backend y organiza la lectura en estado general, observaciones técnicas, rendimiento básico, SEO y oportunidades de mejora.",
        "is_live": True,
        "group_key": "diagnostics",
        "cta_label": "Abrir AI Auditor",
        "recommended_for": ["Auditoría inicial de una URL", "Revisión SEO básica", "Diagnóstico técnico previo a cambios"],
        "related_slugs": ["landing-performance-snapshot", "adtech-debug-tool", "utm-builder"],
        "related_context": "Si necesitas una lectura más corta o una revisión específica de monetización visible, estas herramientas completan el análisis.",
        "capabilities": [
            "Hace una lectura HTTP y HTML básica desde backend.",
            "Puede sumar datos de PageSpeed si la integración está disponible.",
            "Mantiene una salida útil aunque las capas externas no respondan.",
        ],
        "inputs": ["Una URL pública con http o https."],
        "outputs": ["Estado general", "Observaciones técnicas", "Rendimiento básico", "SEO básico", "Oportunidades detectadas", "Recomendación general"],
        "detail_blocks": [
            {
                "title": "Qué hace esta versión",
                "items": [
                    "Lee una URL pública desde backend e intenta extraer señales técnicas básicas.",
                    "Usa PageSpeed cuando la API devuelve datos válidos.",
                    "Ordena la salida por hallazgos, prioridades y siguiente paso sugerido.",
                ],
            },
            {
                "title": "Qué no hace",
                "items": [
                    "No reemplaza una auditoría técnica profunda.",
                    "No recorre múltiples páginas ni hace crawling.",
                    "No depende de OpenAI para funcionar.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "Qué analiza AI Auditor",
            "analysis_items": [
                "Estado HTTP, tiempo de respuesta y URL final.",
                "Metadatos básicos como title, meta description, canonical y robots.",
                "Cantidad de H1 y señales iniciales de estructura HTML.",
                "Puntajes de rendimiento y SEO si PageSpeed está disponible.",
            ],
            "use_title": "Cuándo conviene usarlo",
            "use_items": [
                "Antes de publicar una landing o una página nueva.",
                "Cuando necesitas una auditoría técnica rápida sin abrir varias herramientas.",
                "Como primer paso antes de pasar a una revisión más profunda de SEO o rendimiento.",
            ],
            "results_title": "Qué resultados devuelve",
            "results_items": [
                "Un resumen técnico con estado general y prioridad.",
                "Observaciones sobre rendimiento, SEO y estructura HTML.",
                "Hallazgos priorizados para copiar o exportar.",
            ],
            "limitations_title": "Limitaciones reales",
            "limitations_items": [
                "La lectura depende de la respuesta inicial del servidor.",
                "Si PageSpeed no responde, el análisis se limita a la capa HTTP y HTML.",
                "No reemplaza una auditoría manual completa ni un análisis multipágina.",
            ],
            "faq_title": "Preguntas frecuentes sobre AI Auditor",
            "faqs": [
                {"question": "¿AI Auditor revisa todo el sitio web?", "answer": "No. Analiza la URL que envías y construye un diagnóstico de primera pasada sobre esa página."},
                {"question": "¿Necesita una API externa para funcionar?", "answer": "No. La herramienta puede operar con la lectura HTTP básica. PageSpeed y OpenAI son capas opcionales."},
                {"question": "¿Sirve para SEO técnico?", "answer": "Sirve como revisión SEO básica. Detecta faltantes visibles y organiza prioridades, pero no reemplaza una auditoría SEO completa."},
            ],
        },
    },
    {
        "slug": "landing-performance-snapshot",
        "name": "Landing Performance Snapshot",
        "tag": "Diagnóstico rápido",
        "status_label": "Activa",
        "status_tone": "live",
        "summary": "Snapshot corto de respuesta, metadatos y fricciones básicas.",
        "description": "Entrega una lectura técnica rápida sobre estado HTTP, tiempo de respuesta, redirecciones, estructura HTML básica y señales simples de calidad para una landing.",
        "seo_title": "Snapshot técnico de landing page | Pi Development",
        "meta_description": "Landing Performance Snapshot revisa estado HTTP, tiempo de respuesta, title, meta description, canonical, robots y H1 de una landing page.",
        "meta_keywords": "análisis de landing page, snapshot técnico, estado HTTP, title y meta description, revisión rápida SEO",
        "page_title": "Snapshot técnico para revisar una landing page",
        "page_description": "Landing Performance Snapshot toma una URL y devuelve una lectura corta sobre respuesta, metadatos y señales básicas de estructura sin convertirla en una auditoría pesada.",
        "is_live": True,
        "group_key": "diagnostics",
        "cta_label": "Abrir Landing Performance Snapshot",
        "recommended_for": ["QA técnico rápido", "Revisión previa a publicación", "Control básico de metadatos"],
        "related_slugs": ["ai-auditor", "utm-builder", "adtech-debug-tool"],
        "related_context": "Si el snapshot deja dudas o aparece una capa técnica específica, estas herramientas permiten profundizar sin cambiar de flujo.",
        "capabilities": [
            "Reutiliza la lectura HTTP compartida para una salida más breve que AI Auditor.",
            "Marca faltantes de title, meta description, canonical, H1 y robots restrictivo.",
            "Entrega una recomendación simple sin depender de servicios externos.",
        ],
        "inputs": ["Una URL pública con http o https."],
        "outputs": ["Estado general", "Estructura básica", "Señales rápidas", "Recomendación simple"],
        "detail_blocks": [
            {
                "title": "Qué hace esta versión",
                "items": [
                    "Lee estado HTTP, tiempo de respuesta y redirecciones.",
                    "Resume title, meta description, canonical, robots y H1.",
                    "Convierte esos datos en señales rápidas para revisión técnica.",
                ],
            },
            {
                "title": "Qué no hace",
                "items": [
                    "No usa PageSpeed ni métricas de laboratorio.",
                    "No inspecciona recursos, peso total ni waterfall de red.",
                    "No reemplaza una auditoría más profunda.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "Qué analiza Landing Performance Snapshot",
            "analysis_items": [
                "Estado HTTP, URL final y tiempo de respuesta.",
                "Title, meta description, canonical y directiva robots.",
                "Cantidad de H1 visibles en la respuesta inicial.",
            ],
            "use_title": "Cuándo conviene usarlo",
            "use_items": [
                "Antes de publicar una landing o una variación nueva.",
                "Cuando necesitas una verificación rápida sin abrir una auditoría completa.",
                "Para detectar faltantes básicos de SEO técnico y estructura HTML.",
            ],
            "results_title": "Qué resultados devuelve",
            "results_items": [
                "Un resumen breve con estado general.",
                "Señales rápidas sobre metadatos y jerarquía.",
                "Una recomendación simple y accionable.",
            ],
            "limitations_title": "Limitaciones reales",
            "limitations_items": [
                "Solo revisa la respuesta inicial desde backend.",
                "No ejecuta JavaScript del navegador.",
                "No mide Core Web Vitals ni peso real de recursos.",
            ],
            "faq_title": "Preguntas frecuentes sobre Landing Performance Snapshot",
            "faqs": [
                {"question": "¿Reemplaza AI Auditor?", "answer": "No. Es una herramienta más rápida y más corta. Si necesitas más profundidad, AI Auditor es el siguiente paso."},
                {"question": "¿Sirve para SEO técnico?", "answer": "Sirve para revisar metadatos y estructura básica, pero no cubre una auditoría SEO completa."},
                {"question": "¿Puede detectar problemas renderizados por JavaScript?", "answer": "No en esta versión. La lectura se basa en la respuesta inicial del servidor."},
            ],
        },
    },
    {
        "slug": "adtech-debug-tool",
        "name": "AdTech Debug Tool",
        "tag": "Diagnóstico AdTech",
        "status_label": "Activa",
        "status_tone": "live",
        "summary": "Diagnóstico inicial de monetización visible desde backend.",
        "description": "Inspecciona una URL pública para detectar señales visibles de GPT, Google Ad Manager, AdSense, Prebid, vendors conocidos, slots e iframes publicitarios.",
        "seo_title": "Diagnóstico AdTech para detectar GPT, Prebid y monetización | Pi Development",
        "meta_description": "AdTech Debug Tool analiza una URL y detecta señales visibles de GPT, Google Ad Manager, AdSense, Prebid, slots e iframes publicitarios.",
        "meta_keywords": "diagnóstico AdTech, detección de GPT, Google Ad Manager, Prebid, monetización web, debug publicitario",
        "page_title": "Diagnóstico AdTech para detectar señales de monetización",
        "page_description": "AdTech Debug Tool revisa una URL desde backend y busca señales visibles de stack publicitario, wrappers, slots, iframes y patrones de monetización.",
        "is_live": True,
        "group_key": "diagnostics",
        "cta_label": "Abrir AdTech Debug Tool",
        "recommended_for": ["Revisión de monetización visible", "Debug inicial de stack publicitario", "Detección de GPT o Prebid"],
        "related_slugs": ["creative-preview-lab", "creative-qa-checklist", "ai-auditor"],
        "related_context": "Si el problema puede venir del código de la pieza o de una implementación más amplia, estas herramientas permiten seguir el rastro.",
        "capabilities": [
            "Detecta patrones de GPT, AdSense, Prebid y vendors conocidos.",
            "Revisa scripts, iframes, slots e indicios de refresh, lazy load o targeting.",
            "Aclara cuándo la lectura es parcial o depende del lado del cliente.",
        ],
        "inputs": ["Una URL pública con http o https."],
        "outputs": ["Estado general", "Señales detectadas de monetización", "Hallazgos técnicos", "Observaciones y oportunidades", "Recomendación general"],
        "detail_blocks": [
            {
                "title": "Qué hace esta versión",
                "items": [
                    "Inspecciona HTML y respuesta inicial desde backend.",
                    "Busca patrones extensibles de scripts, wrappers, slots e iframes publicitarios.",
                    "Aclara cuándo parte del stack parece cargarse solo del lado del cliente.",
                ],
            },
            {
                "title": "Qué no hace",
                "items": [
                    "No ejecuta JavaScript en un navegador real.",
                    "No captura requests de red ni comportamiento en runtime.",
                    "No garantiza visibilidad total si la implementación es completamente client-side.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "Qué analiza AdTech Debug Tool",
            "analysis_items": [
                "Señales de GPT, Google Ad Manager, AdSense y Prebid.",
                "Scripts, iframes, slots y wrappers publicitarios conocidos.",
                "Patrones de refresh, lazy load o targeting cuando son visibles en el HTML inicial.",
            ],
            "use_title": "Cuándo conviene usarlo",
            "use_items": [
                "Cuando necesitas confirmar si una URL expone stack publicitario visible.",
                "Para una primera revisión de monetización sin abrir el navegador.",
                "Como punto de partida antes de escalar a una revisión manual más profunda.",
            ],
            "results_title": "Qué resultados devuelve",
            "results_items": [
                "Un estado general de lectura AdTech.",
                "Señales detectadas, evidencia visible y observaciones técnicas.",
                "Una recomendación basada en lo que realmente se pudo ver desde backend.",
            ],
            "limitations_title": "Limitaciones reales",
            "limitations_items": [
                "La detección se basa en el HTML inicial y no ejecuta JavaScript.",
                "Parte del stack puede quedar oculta si se monta completamente del lado del cliente.",
                "No valida serving real ni requests publicitarios en red.",
            ],
            "faq_title": "Preguntas frecuentes sobre AdTech Debug Tool",
            "faqs": [
                {"question": "¿Detecta Google Ad Manager y GPT?", "answer": "Sí. Busca señales visibles compatibles con GPT y con rutas frecuentes de Google Ad Manager."},
                {"question": "¿Si no detecta señales significa que no hay monetización?", "answer": "No necesariamente. La herramienta solo confirma lo que es visible en la respuesta inicial desde backend."},
                {"question": "¿Puede revisar header bidding?", "answer": "Sí, en la medida en que aparezcan señales de Prebid u otras bibliotecas en el HTML descargado."},
            ],
        },
    },
]

OPERATION_AND_QA_TOOLS = [
    {
        "slug": "utm-builder",
        "name": "UTM Builder",
        "tag": "Etiquetado",
        "status_label": "Activa",
        "status_tone": "live",
        "summary": "Generador de URLs con parámetros UTM consistentes.",
        "description": "Construye URLs con parámetros UTM sin romper query params existentes y deja una salida clara para copiar, validar y compartir.",
        "seo_title": "Generador de URLs con parámetros UTM | Pi Development",
        "meta_description": "UTM Builder construye URLs con parámetros UTM consistentes, preserva query params existentes y evita errores comunes de etiquetado.",
        "meta_keywords": "generador UTM, constructor de URLs UTM, parámetros utm, etiquetado de campañas, url tracking",
        "page_title": "Generador de URLs con parámetros UTM",
        "page_description": "UTM Builder arma URLs etiquetadas, conserva parámetros previos y muestra qué campos faltan para mantener un etiquetado analítico consistente.",
        "is_live": True,
        "group_key": "operations",
        "cta_label": "Abrir UTM Builder",
        "recommended_for": ["Etiquetado de campañas", "Trafficking", "Control de URLs con tracking"],
        "related_slugs": ["landing-performance-snapshot", "ai-auditor", "creative-qa-checklist"],
        "related_context": "Si la URL final también necesita revisión técnica o control de QA, estas herramientas completan el flujo.",
        "capabilities": [
            "Reconstruye URLs sin perder query params existentes.",
            "Normaliza valores UTM para reducir errores manuales.",
            "Marca cuando faltan source, medium o campaign.",
        ],
        "inputs": ["URL de destino", "utm_source, utm_medium, utm_campaign", "utm_term y utm_content opcionales"],
        "outputs": ["URL final construida", "Vista previa de parámetros", "Observaciones de etiquetado"],
        "detail_blocks": [
            {
                "title": "Qué hace esta versión",
                "items": [
                    "Valida la URL de destino y reconstruye la query de forma segura.",
                    "Preserva parámetros existentes y agrega solo las claves UTM completadas.",
                    "Señala campos base faltantes antes de compartir la URL.",
                ],
            },
            {
                "title": "Qué puede sumar una versión futura",
                "items": [
                    "Plantillas por canal o cliente.",
                    "Presets de nomenclatura.",
                    "Generación masiva de URLs.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "Qué hace UTM Builder",
            "analysis_items": [
                "Valida la URL de destino antes de construir la salida.",
                "Conserva query params existentes que no pertenezcan a UTM.",
                "Añade únicamente los parámetros UTM que completas en el formulario.",
            ],
            "use_title": "Cuándo conviene usarlo",
            "use_items": [
                "Antes de lanzar campañas con seguimiento por fuente, medio y campaña.",
                "Cuando necesitas compartir URLs limpias con un criterio consistente de tracking.",
                "Para revisar si una URL ya trae parámetros UTM o si queda incompleta.",
            ],
            "results_title": "Qué resultados devuelve",
            "results_items": [
                "La URL final lista para copiar.",
                "Una vista clara de los parámetros aplicados y preservados.",
                "Observaciones sobre campos faltantes o sobrescritura de UTM existentes.",
            ],
            "limitations_title": "Limitaciones reales",
            "limitations_items": [
                "No valida taxonomías internas ni convenciones de naming de cada equipo.",
                "No guarda presets ni genera lotes en esta versión.",
                "No sustituye una gobernanza analítica si el naming cambia entre campañas.",
            ],
            "faq_title": "Preguntas frecuentes sobre UTM Builder",
            "faqs": [
                {"question": "¿La herramienta elimina parámetros que ya existen?", "answer": "No. Conserva los parámetros existentes salvo que envíes un UTM con la misma clave."},
                {"question": "¿Puedo dejar campos vacíos?", "answer": "Sí. Los campos opcionales pueden quedar vacíos y la herramienta no inventa valores."},
                {"question": "¿Sirve para cualquier URL?", "answer": "Sí, siempre que la URL sea pública y use http o https."},
            ],
        },
    },
    {
        "slug": "creative-qa-checklist",
        "name": "Creative QA Checklist",
        "tag": "QA técnico",
        "status_label": "Activa",
        "status_tone": "live",
        "summary": "Checklist técnico para revisar creatividades y tags.",
        "description": "Convierte datos manuales de una creatividad en una lectura técnica inicial con checklist, observaciones, alertas y estado final.",
        "seo_title": "Checklist técnico para validar creatividades | Pi Development",
        "meta_description": "Creative QA Checklist revisa dimensiones, click path, tracking, peso, autoplay y contexto de serving para evaluar una creatividad.",
        "meta_keywords": "validación de creatividades, checklist técnico, qa de banners, click path, tracking publicitario",
        "page_title": "Checklist técnico para validar creatividades publicitarias",
        "page_description": "Creative QA Checklist ordena la revisión inicial de una creatividad con reglas simples sobre dimensiones, click path, tracking, peso, reproducción y contexto de serving.",
        "is_live": True,
        "group_key": "qa_preview",
        "cta_label": "Abrir Creative QA Checklist",
        "recommended_for": ["Preflight de creatividades", "QA previo a trafficking", "Revisión técnica inicial"],
        "related_slugs": ["creative-preview-lab", "adtech-debug-tool", "utm-builder"],
        "related_context": "Si necesitas ver la pieza en una vista previa o revisar el stack publicitario donde podría servirse, estas herramientas siguen el mismo flujo.",
        "capabilities": [
            "Evalúa click path, tracking, peso, contexto y reproducción.",
            "Entrega estado final con criterio transparente.",
            "Separa puntos correctos, observaciones y alertas fuertes.",
        ],
        "inputs": ["Datos manuales de la creatividad", "URL, peso, contexto y reproducción", "Notas opcionales"],
        "outputs": ["Checklist estructurado", "Observaciones y alertas", "Estado final de QA"],
        "detail_blocks": [
            {
                "title": "Qué hace esta versión",
                "items": [
                    "Toma datos manuales y aplica reglas simples pero útiles.",
                    "Distingue entre puntos correctos, observaciones y alertas de bloqueo.",
                    "Muestra con claridad qué debe revisarse antes de aprobar.",
                ],
            },
            {
                "title": "Qué no hace",
                "items": [
                    "No inspecciona archivos binarios ni manifiestos reales.",
                    "No valida la carga de recursos en red.",
                    "No reemplaza una revisión operativa final de trafficking.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "Qué analiza Creative QA Checklist",
            "analysis_items": [
                "Dimensiones declaradas, click path y URL de destino.",
                "Tracking adicional, peso del asset y dispositivo objetivo.",
                "Comportamiento de audio, autoplay y contexto de serving.",
            ],
            "use_title": "Cuándo conviene usarlo",
            "use_items": [
                "Antes de aprobar una creatividad para trafficking.",
                "Cuando necesitas una validación rápida basada en reglas claras.",
                "Para documentar observaciones técnicas sin abrir una hoja de control aparte.",
            ],
            "results_title": "Qué resultados devuelve",
            "results_items": [
                "Estado final: lista, necesita revisión o bloqueada.",
                "Checklist con detalle por criterio.",
                "Observaciones y alertas priorizadas.",
            ],
            "limitations_title": "Limitaciones reales",
            "limitations_items": [
                "Depende de los datos manuales cargados en el formulario.",
                "No inspecciona el archivo fuente ni verifica la ejecución real.",
                "No valida compatibilidad por ad server o plataforma específica.",
            ],
            "faq_title": "Preguntas frecuentes sobre Creative QA Checklist",
            "faqs": [
                {"question": "¿Puedo usarla sin tener el archivo final?", "answer": "Sí. La herramienta está pensada para una revisión inicial basada en datos manuales."},
                {"question": "¿Marca bloqueos reales?", "answer": "Sí. Algunas reglas, como autoplay con sonido o ausencia total de click path, se consideran bloqueantes."},
                {"question": "¿Sirve para cualquier formato?", "answer": "Sirve para una primera revisión de varios formatos, pero no cubre todas las particularidades de cada plataforma."},
            ],
        },
    },
    {
        "slug": "creative-preview-lab",
        "name": "Creative Preview Lab",
        "tag": "Vista previa y QA",
        "status_label": "Activa",
        "status_tone": "live",
        "summary": "Vista previa controlada para creatividades HTML y tags.",
        "description": "Permite pegar markup o tags de terceros, definir dimensiones y obtener una vista previa contenida junto a una lectura técnica básica y honesta.",
        "seo_title": "Vista previa de creatividades HTML y tags publicitarios | Pi Development",
        "meta_description": "Creative Preview Lab renderiza creatividades HTML y tags publicitarios en un sandbox controlado y detecta scripts, iframes, enlaces y limitaciones técnicas.",
        "meta_keywords": "preview de creatividades html, validador de tags publicitarios, sandbox html, revisión de banners, vista previa third-party tag",
        "page_title": "Vista previa de creatividades HTML y tags publicitarios",
        "page_description": "Creative Preview Lab permite pegar código HTML o tags de terceros, renderizar una vista previa en un sandbox y recibir una lectura técnica básica sobre scripts, iframes, enlaces y limitaciones.",
        "is_live": True,
        "group_key": "qa_preview",
        "cta_label": "Abrir Creative Preview Lab",
        "recommended_for": ["Vista previa rápida de markup", "Revisión inicial de tags de terceros", "QA visual antes de escalar"],
        "related_slugs": ["creative-qa-checklist", "adtech-debug-tool", "landing-performance-snapshot"],
        "related_context": "Si después de la vista previa necesitas validar criterios de QA o revisar la capa AdTech, estas herramientas completan la revisión.",
        "capabilities": [
            "Renderiza código dentro de un iframe con sandbox.",
            "Detecta scripts, iframes, enlaces, medios, referencias externas y macros visibles.",
            "Aclara cuándo la vista previa es parcial, bloqueada o depende de un entorno externo.",
        ],
        "inputs": ["Tipo de pieza", "Ancho y alto", "Modo de entrada", "Código HTML o tag", "URL de clic y notas opcionales"],
        "outputs": ["Estado de la vista previa", "Elementos detectados", "Observaciones técnicas", "Recomendación final"],
        "detail_blocks": [
            {
                "title": "Qué hace esta versión",
                "items": [
                    "Recibe markup o tags de terceros y los renderiza dentro de un iframe controlado.",
                    "Entrega hallazgos técnicos inmediatos sin prometer validación total.",
                    "Explica cuándo la vista previa es parcial o está bloqueada por seguridad.",
                ],
            },
            {
                "title": "Qué no hace",
                "items": [
                    "No simula el comportamiento real de un ad server.",
                    "No valida tracking de red ni clics reales.",
                    "No replica SafeFrame ni entornos propietarios.",
                ],
            },
        ],
        "editorial": {
            "analysis_title": "Qué analiza Creative Preview Lab",
            "analysis_items": [
                "Scripts, iframes, enlaces, recursos externos y etiquetas multimedia.",
                "Macros, placeholders y patrones que limitan la vista previa.",
                "Dimensiones declaradas y estado general del render.",
            ],
            "use_title": "Cuándo conviene usarlo",
            "use_items": [
                "Cuando necesitas revisar código HTML o un tag en pocos segundos.",
                "Antes de pasar una pieza a una revisión técnica más profunda.",
                "Para detectar de inmediato si la vista previa es parcial o insegura.",
            ],
            "results_title": "Qué resultados devuelve",
            "results_items": [
                "Una vista previa renderizada, parcial, bloqueada o vacía.",
                "Conteo de elementos detectados dentro del código.",
                "Observaciones y limitaciones técnicas para una primera revisión.",
            ],
            "limitations_title": "Limitaciones reales",
            "limitations_items": [
                "No replica SafeFrame ni el comportamiento de un ad server real.",
                "Los scripts externos pueden quedar bloqueados o renderizar de forma parcial.",
                "No verifica tracking, clics reales ni compatibilidad total.",
            ],
            "faq_title": "Preguntas frecuentes sobre Creative Preview Lab",
            "faqs": [
                {"question": "¿La vista previa replica exactamente el ad server?", "answer": "No. Es una vista previa controlada para revisión inicial, no una simulación exacta del serving real."},
                {"question": "¿Puede bloquear un código?", "answer": "Sí. Si detecta patrones de escape del frame o navegación insegura, bloquea la ejecución visual y mantiene el análisis técnico."},
                {"question": "¿Sirve para tags de terceros?", "answer": "Sí, pero la ejecución puede ser parcial si depende de recursos externos o de un entorno propietario."},
            ],
        },
    },
]

TOOL_DEFINITIONS = DIAGNOSTIC_TOOLS + OPERATION_AND_QA_TOOLS


def get_tools_index_page():
    return deepcopy(TOOLS_INDEX_PAGE)


def get_tools():
    return deepcopy(TOOL_DEFINITIONS)


def get_featured_tool():
    return deepcopy(TOOL_DEFINITIONS[0])


def get_tool(slug):
    for tool in TOOL_DEFINITIONS:
        if tool["slug"] == slug:
            return deepcopy(tool)
    return None


def get_public_tool_slugs():
    return [tool["slug"] for tool in TOOL_DEFINITIONS]


def get_tool_groups():
    groups = []
    for group_key, group_meta in TOOL_GROUPS.items():
        group_tools = [deepcopy(tool) for tool in TOOL_DEFINITIONS if tool.get("group_key") == group_key]
        if group_tools:
            groups.append(
                {
                    "key": group_meta["key"],
                    "title": group_meta["title"],
                    "description": group_meta["description"],
                    "tools": group_tools,
                }
            )
    return groups


def get_related_tools(slug, limit=3):
    current_tool = next((tool for tool in TOOL_DEFINITIONS if tool["slug"] == slug), None)
    if not current_tool:
        return []

    related_slugs = list(current_tool.get("related_slugs") or [])
    ordered_slugs = related_slugs + [
        tool["slug"] for tool in TOOL_DEFINITIONS if tool["slug"] not in related_slugs and tool["slug"] != slug
    ]
    related_tools = []

    for related_slug in ordered_slugs:
        if related_slug == slug:
            continue
        tool = get_tool(related_slug)
        if tool:
            related_tools.append(tool)
        if len(related_tools) >= limit:
            break

    return related_tools
