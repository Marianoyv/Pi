from copy import deepcopy


SEO_PAGE_DEFINITIONS = [
    {
        "slug": "validar-creatividad-html",
        "title": "Como validar una creatividad HTML antes de trafficking | Pi Development",
        "meta_description": "Guia tecnica para validar una creatividad HTML: dimensiones, clickTag, tracking, peso, autoplay y dependencias antes de aprobar una pieza.",
        "meta_keywords": "validar creatividad html, qa creatividad html, revisar banner html5, clicktag, tracking publicitario",
        "eyebrow": "QA de creatividades",
        "h1": "Como validar una creatividad HTML antes de trafficking",
        "description": "Esta pagina resume los controles tecnicos que conviene hacer sobre una creatividad HTML antes de enviarla a trafficking o subirla a una plataforma.",
        "intro_paragraphs": [
            "Validar una creatividad HTML no consiste solo en abrir el archivo y comprobar que se vea. En una revision tecnica conviene revisar dimensiones, clickTag, dependencias externas, peso, comportamiento multimedia y trazas de tracking.",
            "Cuando esa validacion se omite, los errores aparecen en serving: piezas que no cargan, clics que no resuelven, medicion incompleta o comportamientos que incumplen politicas de autoplay. La idea de esta guia es ordenar esa primera pasada con un criterio util.",
        ],
        "common_problems": [
            {
                "title": "Click path incompleto o ambiguo",
                "text": "La pieza declara un enlace, pero no queda claro si usa clickTag, macro de plataforma o una URL hardcodeada que puede romper el flujo de serving.",
            },
            {
                "title": "Markup dependiente de recursos externos",
                "text": "Scripts, fuentes, videos o imagenes remotas pueden bloquear el render o alterar el comportamiento final si el entorno de serving no replica el entorno de desarrollo.",
            },
            {
                "title": "Autoplay, peso o dimensiones fuera de criterio",
                "text": "Una creatividad puede verse correcta y aun asi fallar por peso excesivo, audio al cargar o dimensiones que no coinciden con el placement previsto.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Separar revision de estructura y revision de serving",
                "text": "Primero valida la pieza en si misma: dimensiones, click path, peso y dependencias. Despues revisa el contexto donde se va a entregar.",
            },
            {
                "title": "Usar una checklist antes de aprobar",
                "text": "Una checklist evita pasar por alto errores repetidos como ausencia de tracking, destino roto o configuraciones de audio no permitidas.",
            },
            {
                "title": "Abrir una vista previa controlada cuando hay HTML o tags",
                "text": "Si el asset incluye scripts o terceros, la vista previa controlada ayuda a distinguir entre un problema del codigo y una limitacion del entorno.",
            },
        ],
        "primary_tool_slug": "creative-qa-checklist",
        "primary_tool_reason": "Creative QA Checklist ordena la validacion inicial de la pieza y marca alertas reales sobre click path, tracking, peso, autoplay y contexto de serving.",
        "related_tool_slugs": ["creative-preview-lab", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Carga los datos base de la pieza",
                "text": "Completa nombre, formato, dimensiones, URL de destino, presencia de click path y peso declarado.",
            },
            {
                "title": "Marca el comportamiento multimedia y el contexto",
                "text": "Indica autoplay, sonido, dispositivo objetivo y si la creatividad correra en SafeFrame, iframe o un contexto todavia incierto.",
            },
            {
                "title": "Revisa alertas y puntos bloqueantes",
                "text": "La herramienta separa observaciones menores de bloqueos que conviene corregir antes de aprobar la creatividad.",
            },
            {
                "title": "Pasa a una vista previa si necesitas ver el markup",
                "text": "Si ademas quieres inspeccionar scripts, iframes o macros visibles, abre Creative Preview Lab como segundo paso.",
            },
        ],
        "faqs": [
            {
                "question": "Que diferencia hay entre validar y hacer preview de una creatividad HTML?",
                "answer": "Validar implica revisar criterios tecnicos y de aprobacion. El preview sirve para ver como responde el markup dentro de un entorno controlado. Lo normal es usar ambos pasos cuando la pieza trae codigo.",
            },
            {
                "question": "Se puede validar una creatividad sin tener el ZIP final?",
                "answer": "Si. Una primera pasada puede hacerse con datos manuales, siempre que declares dimensiones, destino, tracking y comportamiento multimedia con precision.",
            },
            {
                "question": "Esta guia reemplaza el QA final de trafficking?",
                "answer": "No. Ordena la validacion previa, pero el QA final sigue dependiendo del ad server, la plataforma y el entorno real de entrega.",
            },
        ],
        "related_page_slugs": [
            "preview-anuncios-html",
            "errores-creatividades-display",
            "como-validar-tags-publicitarios",
        ],
    },
    {
        "slug": "preview-anuncios-html",
        "title": "Preview de anuncios HTML en un entorno controlado | Pi Development",
        "meta_description": "Como previsualizar anuncios HTML y tags de terceros sin depender del ad server: iframe sandbox, scripts, iframes, macros y limites reales.",
        "meta_keywords": "preview anuncios html, vista previa banner html, preview tag publicitario, sandbox html, rich media preview",
        "eyebrow": "Vista previa tecnica",
        "h1": "Preview de anuncios HTML y rich media",
        "description": "Si necesitas revisar markup publicitario antes de integrarlo, esta guia explica que conviene mirar en una vista previa controlada y que no deberias asumir.",
        "intro_paragraphs": [
            "Un preview de anuncios HTML sirve para responder una pregunta concreta: el codigo renderiza de forma legible dentro de un contenedor controlado o ya expone problemas visibles en la primera carga.",
            "Eso no equivale a replicar SafeFrame, un ad server o todos los eventos de un entorno real. La utilidad del preview esta en detectar scripts, iframes, enlaces, macros o bloqueos inmediatos antes de escalar a una revision mas costosa.",
        ],
        "common_problems": [
            {
                "title": "La pieza solo funciona dentro de un entorno propietario",
                "text": "Muchos tags dependen de variables, macros o permisos que no existen en una vista previa generica, por lo que el render puede quedar parcial o vacio.",
            },
            {
                "title": "Scripts o iframes externos quedan bloqueados",
                "text": "El browser puede restringir recursos de terceros, y eso hace visible una limitacion tecnica que conviene documentar antes de aprobar la pieza.",
            },
            {
                "title": "Se asume que el preview replica el serving real",
                "text": "Un preview controlado ayuda a inspeccionar markup, pero no garantiza clics, medicion, refresh ni el comportamiento exacto del stack publicitario.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Definir dimensiones y modo de entrada antes de renderizar",
                "text": "La lectura tecnica mejora si la pieza entra con un tamaño claro y si distingues entre HTML propio y tag de terceros.",
            },
            {
                "title": "Leer el preview junto con los elementos detectados",
                "text": "No basta con mirar si se ve algo. Conviene revisar cuantos scripts, iframes, enlaces, macros o recursos externos aparecen en el codigo.",
            },
            {
                "title": "Escalar a QA o debug segun el problema",
                "text": "Si el problema es de la pieza, pasa a una checklist de QA. Si sospechas una limitacion del stack publicitario, revisa la pagina con una herramienta AdTech.",
            },
        ],
        "primary_tool_slug": "creative-preview-lab",
        "primary_tool_reason": "Creative Preview Lab permite pegar HTML o tags publicitarios, renderizar una vista previa en sandbox y recibir hallazgos tecnicos inmediatos sobre scripts, iframes, enlaces y macros.",
        "related_tool_slugs": ["creative-qa-checklist", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Selecciona tipo de pieza y dimensiones",
                "text": "Declara si estas probando display, rich media o tag de terceros, y define ancho y alto para el contenedor.",
            },
            {
                "title": "Pega el markup o el tag",
                "text": "Usa HTML si controlas el codigo o el modo third-party si estas revisando un snippet entregado por un vendor.",
            },
            {
                "title": "Lee el estado del render",
                "text": "La salida te indica si la vista previa fue correcta, parcial, bloqueada o vacia. Esa distincion evita interpretar mal el resultado.",
            },
            {
                "title": "Revisa limitaciones y decide el siguiente paso",
                "text": "Si el preview es parcial por dependencias externas, documentalo y completa la revision con QA tecnico o debug del entorno.",
            },
        ],
        "faqs": [
            {
                "question": "Un preview correcto significa que la pieza ya esta lista para servir?",
                "answer": "No necesariamente. Significa que el markup renderizo dentro del sandbox. Todavia falta validar serving, tracking, clics y compatibilidad en el entorno real.",
            },
            {
                "question": "Por que algunos tags quedan en blanco?",
                "answer": "Porque dependen de recursos externos, macros o permisos que no existen fuera del entorno propietario donde normalmente se ejecutan.",
            },
            {
                "question": "Conviene usar preview y checklist juntos?",
                "answer": "Si. El preview muestra el comportamiento visual y la checklist ordena la aprobacion tecnica de la pieza.",
            },
        ],
        "related_page_slugs": [
            "validar-creatividad-html",
            "como-validar-tags-publicitarios",
            "errores-creatividades-display",
        ],
    },
    {
        "slug": "debug-anuncios-web",
        "title": "Como debuggear anuncios web y stack publicitario visible | Pi Development",
        "meta_description": "Guia para debuggear anuncios web: senales de GPT, Prebid, wrappers, slots, iframes y lecturas visibles desde backend.",
        "meta_keywords": "debug anuncios web, diagnostico publicitario, revisar gpt, prebid debug, stack publicitario",
        "eyebrow": "Diagnostico AdTech",
        "h1": "Como debuggear anuncios web y la implementacion publicitaria visible",
        "description": "Cuando una pagina monetizada no se comporta como esperas, conviene separar problemas de stack publicitario, problemas de markup y problemas de serving real.",
        "intro_paragraphs": [
            "Debuggear anuncios web implica identificar que senales del stack publicitario son realmente visibles en la pagina y cuales solo aparecen durante la ejecucion del navegador.",
            "La primera lectura util suele apoyarse en el HTML inicial: scripts de GPT o Prebid, wrappers conocidos, iframes, hints de slots y otros patrones que ayudan a saber por donde empezar la revision.",
        ],
        "common_problems": [
            {
                "title": "No queda claro si la pagina carga GPT, Prebid o ambos",
                "text": "En implementaciones mixtas es facil perder tiempo buscando en el lugar equivocado si no confirmas primero que librerias aparecen en la respuesta inicial.",
            },
            {
                "title": "Los slots no son legibles en el HTML",
                "text": "Puede haber scripts publicitarios visibles, pero sin una estructura clara de contenedores o identifiers que ayuden a mapear placements.",
            },
            {
                "title": "Parte del stack solo existe del lado del cliente",
                "text": "Si gran parte de la implementacion se monta en runtime, una lectura backend alcanza para detectar indicios, no para confirmar serving completo.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Empezar por la respuesta inicial",
                "text": "Confirma primero si aparecen scripts, vendors, wrappers, iframes o patrones de monetizacion antes de ir a una inspeccion manual mas profunda.",
            },
            {
                "title": "Separar senales visibles de hipotesis",
                "text": "Lo importante no es adivinar todo el stack, sino documentar con claridad que componentes se vieron y que parte sigue siendo incierta.",
            },
            {
                "title": "Cruzar el hallazgo con la pieza cuando haga falta",
                "text": "Si la pagina carga stack publicitario pero la creatividad falla, el siguiente paso suele ser revisar la pieza o el tag en paralelo.",
            },
        ],
        "primary_tool_slug": "adtech-debug-tool",
        "primary_tool_reason": "AdTech Debug Tool inspecciona una URL publica y detecta senales visibles de GPT, Google Ad Manager, Prebid, vendors conocidos, slots e iframes publicitarios.",
        "related_tool_slugs": ["ai-auditor", "creative-preview-lab"],
        "how_to_use": [
            {
                "title": "Carga la URL de la pagina con anuncios",
                "text": "Usa una URL publica que exponga el HTML inicial del placement o de la pagina monetizada que quieres revisar.",
            },
            {
                "title": "Lee las senales detectadas",
                "text": "La herramienta lista patrones compatibles con GPT, Prebid, AdSense, wrappers y otras senales visibles desde backend.",
            },
            {
                "title": "Revisa hallazgos y limitaciones",
                "text": "Cuando la lectura es parcial, la salida lo aclara. Eso evita sacar conclusiones demasiado fuertes a partir de un HTML incompleto.",
            },
            {
                "title": "Pasa a preview o QA si el problema apunta a la pieza",
                "text": "Si el stack parece presente pero la creatividad no responde, completa la revision con Creative Preview Lab o Creative QA Checklist.",
            },
        ],
        "faqs": [
            {
                "question": "La herramienta confirma el serving real de los anuncios?",
                "answer": "No. Confirma senales visibles en la respuesta inicial. El serving real y la red de requests siguen necesitando una revision en navegador.",
            },
            {
                "question": "Puede detectar Prebid aunque la pagina renderice mucho con JavaScript?",
                "answer": "Si la libreria o sus patrones aparecen en el HTML descargado, si. Si todo se monta del lado del cliente, la lectura puede ser parcial.",
            },
            {
                "question": "Cuando conviene combinar debug de pagina y preview de tag?",
                "answer": "Cuando el problema puede venir tanto del entorno publicitario como del codigo de la creatividad o del tag de terceros.",
            },
        ],
        "related_page_slugs": [
            "debug-gpt-ads",
            "como-validar-tags-publicitarios",
            "herramientas-adtech",
        ],
    },
    {
        "slug": "debug-gpt-ads",
        "title": "Debug de GPT Ads y Google Publisher Tag | Pi Development",
        "meta_description": "Como revisar senales visibles de Google Publisher Tag, Google Ad Manager, slots e iframes publicitarios en una URL publica.",
        "meta_keywords": "debug gpt ads, google publisher tag, google ad manager debug, revisar slots gpt, anuncios gpt",
        "eyebrow": "Google Publisher Tag",
        "h1": "Como hacer debug de GPT Ads en una pagina web",
        "description": "Esta guia se centra en una pregunta concreta: la pagina expone senales visibles compatibles con Google Publisher Tag y una estructura minima de slots publicitarios.",
        "intro_paragraphs": [
            "Cuando se habla de debug de GPT Ads, muchas veces se mezclan tres capas distintas: presencia de la libreria GPT, configuracion de slots y serving efectivo desde Google Ad Manager.",
            "Una primera lectura tecnica no reemplaza DevTools, pero sirve para detectar si la pagina ya expone scripts de GPT, iframes publicitarios o patrones que justifican profundizar en ese stack.",
        ],
        "common_problems": [
            {
                "title": "GPT esta cargado pero los slots no son evidentes",
                "text": "Puede aparecer la libreria de GPT y aun asi no quedar claro donde se definen los contenedores o como se organiza el inventario visible.",
            },
            {
                "title": "La pagina mezcla GPT con wrappers o header bidding",
                "text": "Cuando coexisten varias capas publicitarias, conviene confirmar primero que se ve en la respuesta inicial para no confundir responsabilidades.",
            },
            {
                "title": "La deteccion backend es parcial",
                "text": "Si buena parte del stack se monta con JavaScript, el analisis backend alcanza a insinuar GPT, pero no siempre a describir toda la secuencia de carga.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Confirmar presencia de la libreria GPT",
                "text": "Busca primero rutas, scripts o patrones de googletag compatibles con Google Publisher Tag.",
            },
            {
                "title": "Revisar evidencia de slots e iframes",
                "text": "Si la pagina expone contenedores, hints de slots o iframes publicitarios, ya tienes una base mejor para inspeccionar el inventario.",
            },
            {
                "title": "Escalar a revision manual solo con una hipotesis clara",
                "text": "La lectura inicial debe ayudarte a decidir si el siguiente paso esta en GAM, en header bidding, en la creatividad o en el runtime del navegador.",
            },
        ],
        "primary_tool_slug": "adtech-debug-tool",
        "primary_tool_reason": "AdTech Debug Tool es la mejor entrada para revisar si una URL expone senales visibles de GPT, Google Ad Manager, slots e iframes publicitarios.",
        "related_tool_slugs": ["creative-preview-lab", "ai-auditor"],
        "how_to_use": [
            {
                "title": "Pega la URL donde deberia correr GPT",
                "text": "Usa la pagina exacta donde el placement o la monetizacion estan generando dudas.",
            },
            {
                "title": "Busca coincidencias de GPT y Google Ad Manager",
                "text": "La salida te muestra scripts y patrones detectados que apuntan a la presencia visible de GPT.",
            },
            {
                "title": "Comprueba si hay slots o iframes visibles",
                "text": "Eso te ayuda a distinguir entre una carga clara del stack y una configuracion demasiado opaca en la respuesta inicial.",
            },
            {
                "title": "Documenta lo visible y lo incierto",
                "text": "Si la herramienta indica limitaciones del render, usa esa informacion para encuadrar mejor una revision manual posterior.",
            },
        ],
        "faqs": [
            {
                "question": "Detectar GPT significa que Google Ad Manager esta sirviendo bien?",
                "answer": "No. Significa que hay senales visibles compatibles con GPT. El serving real requiere confirmar requests, slots y respuesta del ad server en navegador.",
            },
            {
                "question": "Sirve para paginas con header bidding?",
                "answer": "Si. La lectura puede mostrar GPT y al mismo tiempo wrappers o bibliotecas de bidding si aparecen en el HTML inicial.",
            },
            {
                "question": "Que hago si la herramienta no detecta GPT pero sospecho que existe?",
                "answer": "Es probable que la implementacion se cargue del lado del cliente o en otra capa. La herramienta entonces sirve como senal de limitacion, no como prueba de ausencia.",
            },
        ],
        "related_page_slugs": [
            "debug-anuncios-web",
            "herramientas-adtech",
            "errores-creatividades-display",
        ],
    },
    {
        "slug": "como-crear-utms",
        "title": "Como crear UTMs sin romper la URL de destino | Pi Development",
        "meta_description": "Guia para crear parametros UTM con criterio tecnico: source, medium, campaign, preservacion de query params y control de nomenclatura.",
        "meta_keywords": "como crear utms, generar utm, parametros utm, url tracking, etiquetado de campanas",
        "eyebrow": "Tracking y operacion",
        "h1": "Como crear UTMs sin romper la URL de destino",
        "description": "Los parametros UTM parecen simples, pero en equipos con varias manos suelen romperse por naming inconsistente, sobrescritura de queries o errores de copiado.",
        "intro_paragraphs": [
            "Crear UTMs no es solo concatenar pares clave-valor al final de una URL. Conviene preservar query params existentes, normalizar nombres y evitar valores ambiguos que despues vuelven inutil la lectura analitica.",
            "Esta guia apunta a un flujo operativo sobrio: construir la URL final, revisar que los parametros base esten presentes y comprobar que la landing de destino siga siendo correcta despues del etiquetado.",
        ],
        "common_problems": [
            {
                "title": "Se pisan query params existentes",
                "text": "Es comun perder parametros importantes de producto, idioma o referer cuando la URL se reconstruye manualmente y sin control.",
            },
            {
                "title": "Cada persona nombra source y campaign distinto",
                "text": "El problema no es tecnico sino operativo: la taxonomia se vuelve inconsistente y luego cuesta leer campanas o comparar resultados.",
            },
            {
                "title": "La URL final queda mal formada",
                "text": "Espacios, mayusculas, valores vacios o duplicacion de UTMs suelen terminar en enlaces incorrectos o medicion poco confiable.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Partir siempre de la URL de destino final",
                "text": "Antes de agregar UTMs, confirma que la landing correcta ya responde y que la URL base no necesita ajustes adicionales.",
            },
            {
                "title": "Completar solo los campos que tienen una convencion clara",
                "text": "source, medium y campaign suelen ser obligatorios. term y content conviene usarlos solo cuando aportan lectura real.",
            },
            {
                "title": "Revisar la URL etiquetada antes de compartirla",
                "text": "Una validacion rapida evita publicar enlaces con queries rotas o nomenclatura incoherente.",
            },
        ],
        "primary_tool_slug": "utm-builder",
        "primary_tool_reason": "UTM Builder reconstruye la URL de forma segura, conserva query params existentes y marca cuando faltan campos base como source, medium o campaign.",
        "related_tool_slugs": ["landing-performance-snapshot", "ai-auditor"],
        "how_to_use": [
            {
                "title": "Pega la URL de destino",
                "text": "Usa la landing final que quieres medir. Si ya trae query params, la herramienta los conserva.",
            },
            {
                "title": "Completa source, medium y campaign",
                "text": "Esos tres campos suelen ser el minimo util para mantener consistencia analitica.",
            },
            {
                "title": "Agrega term o content solo si aportan lectura",
                "text": "No conviene llenar campos opcionales por inercia. Mejor usarlos cuando diferencian creatividad, keyword o variante.",
            },
            {
                "title": "Copia la URL final y valida la landing",
                "text": "Si quieres una segunda verificacion tecnica, puedes pasar la URL etiquetada por Landing Performance Snapshot o AI Auditor.",
            },
        ],
        "faqs": [
            {
                "question": "La herramienta elimina parametros que ya estaban en la URL?",
                "answer": "No. Preserva query params existentes y solo sobrescribe una clave si envias un UTM con ese mismo nombre.",
            },
            {
                "question": "Conviene poner mayusculas o espacios en los UTMs?",
                "answer": "Lo habitual es normalizar a valores consistentes y legibles. Evitar espacios y cambios arbitrarios ayuda a sostener la taxonomia.",
            },
            {
                "question": "Despues de crear UTMs conviene revisar la landing?",
                "answer": "Si, sobre todo cuando la URL de destino ya es compleja o cuando la campana depende de una landing con reglas tecnicas delicadas.",
            },
        ],
        "related_page_slugs": [
            "auditoria-tecnica-web",
            "analizar-seo-pagina",
            "herramientas-adtech",
        ],
    },
    {
        "slug": "auditoria-tecnica-web",
        "title": "Auditoria tecnica web para detectar problemas visibles | Pi Development",
        "meta_description": "Como hacer una auditoria tecnica web de primera pasada: estado HTTP, respuesta, metadatos, estructura HTML y oportunidades de mejora.",
        "meta_keywords": "auditoria tecnica web, analisis tecnico web, revisar url, diagnostico web, seo tecnico basico",
        "eyebrow": "Diagnostico web",
        "h1": "Auditoria tecnica web de primera pasada",
        "description": "Una auditoria tecnica web inicial sirve para ordenar prioridades antes de entrar en una revision mas profunda de rendimiento, SEO o monetizacion.",
        "intro_paragraphs": [
            "En una primera pasada conviene revisar lo que realmente se puede leer desde una URL publica: estado HTTP, tiempo de respuesta, metadatos centrales, estructura HTML basica y algunos indicios de calidad tecnica.",
            "Ese tipo de auditoria no reemplaza un crawling, un analisis multipagina ni una revision de browser, pero permite detectar faltantes evidentes y definir por donde seguir trabajando.",
        ],
        "common_problems": [
            {
                "title": "La URL responde, pero la base tecnica no esta clara",
                "text": "Es frecuente encontrar paginas publicadas con title poco util, meta description ausente, canonical faltante o una jerarquia HTML confusa.",
            },
            {
                "title": "No hay una priorizacion util de hallazgos",
                "text": "Sin una lectura ordenada, los equipos terminan mezclando observaciones menores con problemas que realmente afectan indexacion o experiencia base.",
            },
            {
                "title": "La revision queda demasiado manual",
                "text": "Abrir varias herramientas para confirmar lo basico consume tiempo y hace mas dificil sostener un chequeo operativo constante.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Leer primero la respuesta HTTP y HTML inicial",
                "text": "Con esa base ya puedes detectar redirects, metadatos ausentes, canonical faltante o H1 multiples sin ir todavia a un analisis mas pesado.",
            },
            {
                "title": "Separar observaciones de oportunidades",
                "text": "Un buen diagnostico no solo enumera problemas: tambien ordena prioridades y siguiente paso recomendado.",
            },
            {
                "title": "Combinar auditoria amplia con snapshots cuando haga falta",
                "text": "Si solo necesitas control rapido de metadatos o estructura, un snapshot corto puede complementar muy bien la auditoria principal.",
            },
        ],
        "primary_tool_slug": "ai-auditor",
        "primary_tool_reason": "AI Auditor organiza una lectura tecnica breve sobre estado general, observaciones, SEO basico, rendimiento y oportunidades para una URL publica.",
        "related_tool_slugs": ["landing-performance-snapshot", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Carga la URL publica",
                "text": "Empieza por la pagina real que quieres revisar, no por un mock o una ruta parcial de desarrollo.",
            },
            {
                "title": "Lee el estado general y las observaciones tecnicas",
                "text": "La herramienta estructura la salida para que distingas salud general, hallazgos tecnicos y oportunidades.",
            },
            {
                "title": "Revisa SEO basico y rendimiento",
                "text": "Si hay faltantes de title, meta description, canonical o problemas de respuesta, quedan visibles en la misma lectura.",
            },
            {
                "title": "Profundiza segun el tipo de hallazgo",
                "text": "Si el problema es de metadata simple, usa Landing Performance Snapshot. Si hay dudas de monetizacion, abre AdTech Debug Tool.",
            },
        ],
        "faqs": [
            {
                "question": "Esta auditoria sirve para todo el sitio?",
                "answer": "No. Sirve para la URL que envias y como punto de partida para definir prioridades. Un sitio completo requiere otra profundidad.",
            },
            {
                "question": "Incluye SEO tecnico?",
                "answer": "Incluye una lectura SEO basica y tecnica sobre la URL analizada, con foco en title, description, canonical, robots y estructura HTML inicial.",
            },
            {
                "question": "Cuando conviene usar un snapshot en vez de una auditoria tecnica?",
                "answer": "Cuando solo necesitas una verificacion rapida de estado, metadatos y estructura basica, sin una lectura mas amplia de oportunidades.",
            },
        ],
        "related_page_slugs": [
            "analizar-seo-pagina",
            "debug-anuncios-web",
            "herramientas-adtech",
        ],
    },
    {
        "slug": "analizar-seo-pagina",
        "title": "Como analizar el SEO de una pagina desde la respuesta inicial | Pi Development",
        "meta_description": "Guia para analizar SEO on-page y tecnico basico: title, meta description, canonical, robots, H1 y estructura HTML visible.",
        "meta_keywords": "analizar seo pagina, seo on page tecnico, title meta description canonical, revisar seo url",
        "eyebrow": "SEO basico",
        "h1": "Como analizar el SEO de una pagina web",
        "description": "Analizar el SEO de una pagina no siempre requiere un crawling completo. Muchas senales utiles se pueden detectar en la respuesta inicial de la URL.",
        "intro_paragraphs": [
            "Para una primera revision SEO conviene observar elementos basicos pero decisivos: title, meta description, canonical, robots y la jerarquia principal del HTML que recibe el usuario o el crawler.",
            "No todo el SEO tecnico se agota ahi, pero esa lectura inicial alcanza para encontrar faltantes evidentes, duplicaciones o configuraciones que afectan indexacion y claridad semantica.",
        ],
        "common_problems": [
            {
                "title": "Title y description ausentes o debiles",
                "text": "Sin esos elementos, la pagina pierde claridad para buscadores y queda peor preparada para captar consultas con una intencion especifica.",
            },
            {
                "title": "Canonical o robots mal resueltos",
                "text": "Una canonical faltante o una directiva restrictiva mal aplicada pueden generar dudas de indexacion incluso en paginas tecnicamente simples.",
            },
            {
                "title": "Jerarquia HTML desordenada",
                "text": "Multiples H1 o una estructura sin foco suelen ser una senal temprana de problemas de arquitectura de contenido.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Empezar con una URL y una lectura concreta",
                "text": "Antes de mirar suites enormes, conviene confirmar si la pagina ya resuelve bien sus metadatos y su estructura principal.",
            },
            {
                "title": "Priorizar faltantes que impactan indexacion",
                "text": "Title, description, canonical, robots y H1 suelen dar una primera lista de tareas mucho mas util que una enumeracion desordenada.",
            },
            {
                "title": "Cruzar SEO basico con estado tecnico",
                "text": "Si la respuesta es lenta, hay redirects extranos o la pagina carga mal, el SEO on-page no deberia analizarse aislado de la base tecnica.",
            },
        ],
        "primary_tool_slug": "ai-auditor",
        "primary_tool_reason": "AI Auditor combina lectura tecnica y SEO basico para una URL publica, con hallazgos ordenados y una recomendacion clara de siguiente paso.",
        "related_tool_slugs": ["landing-performance-snapshot", "utm-builder"],
        "how_to_use": [
            {
                "title": "Carga la URL que quieres revisar",
                "text": "Usa la pagina concreta que quieres posicionar o diagnosticar, no una homepage generica si el problema vive en una URL especifica.",
            },
            {
                "title": "Revisa title, description, canonical y robots",
                "text": "Esos cuatro campos suelen explicar gran parte de los problemas de SEO tecnico visible en una primera pasada.",
            },
            {
                "title": "Comprueba la estructura HTML basica",
                "text": "El conteo de H1 y la lectura del HTML inicial ayudan a detectar una jerarquia editorial debil o inconsistente.",
            },
            {
                "title": "Si necesitas una lectura mas corta, usa el snapshot",
                "text": "Landing Performance Snapshot sirve cuando solo quieres comprobar metadatos y estructura sin pasar por una auditoria mas amplia.",
            },
        ],
        "faqs": [
            {
                "question": "Analizar el SEO de una pagina es lo mismo que hacer una auditoria completa?",
                "answer": "No. Esta guia cubre una lectura inicial y on-page. Una auditoria completa requiere mas contexto, mas URLs y otras capas de analisis.",
            },
            {
                "question": "Conviene revisar SEO aunque la pagina ya este indexada?",
                "answer": "Si. Una pagina indexada puede seguir teniendo metadatos debiles, canonical ausente o estructura HTML poco clara.",
            },
            {
                "question": "Las UTMs afectan este analisis?",
                "answer": "Pueden afectar la lectura operativa de URLs compartidas. Por eso tiene sentido revisar etiquetado y version final de la landing cuando forman parte del flujo.",
            },
        ],
        "related_page_slugs": [
            "auditoria-tecnica-web",
            "como-crear-utms",
            "herramientas-adtech",
        ],
    },
    {
        "slug": "errores-creatividades-display",
        "title": "Errores frecuentes en creatividades display y como detectarlos | Pi Development",
        "meta_description": "Errores comunes en creatividades display: dimensiones, click path, tracking, autoplay, peso, recursos externos y contexto de serving.",
        "meta_keywords": "errores creatividades display, qa banners, problemas html5 ads, clicktag, autoplay creative",
        "eyebrow": "Problemas comunes",
        "h1": "Errores frecuentes en creatividades display",
        "description": "Gran parte de los rechazos o fallos en campanas display se explican por un conjunto bastante repetible de errores tecnicos previos al trafficking.",
        "intro_paragraphs": [
            "En creatividades display el problema no siempre es espectacular. A menudo se trata de detalles tecnicos previsibles: dimensiones mal declaradas, click path dudoso, tracking incompleto, peso excesivo o autoplay fuera de politica.",
            "Por eso conviene trabajar con una revision corta pero consistente que permita bloquear lo importante antes de que la pieza llegue a serving, QA final o publicacion.",
        ],
        "common_problems": [
            {
                "title": "Dimensiones y formato no coinciden con el placement",
                "text": "Una creatividad puede verse bien por separado y aun asi ser inutil si no respeta el inventario o el formato donde se va a servir.",
            },
            {
                "title": "Tracking o click path sin validar",
                "text": "Ausencia de clickTag, macros mal resueltas o URL de destino no revisada son errores operativos muy habituales.",
            },
            {
                "title": "Recursos pesados o comportamiento bloqueante",
                "text": "Peso alto, autoplay con sonido o dependencias externas fragiles suelen convertirse en rechazo tecnico o mala experiencia de carga.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Aplicar una checklist antes del preview",
                "text": "Primero conviene ordenar los criterios de aprobacion y despues mirar el render de la pieza. Asi evitas que un preview correcto tape un problema de policy o tracking.",
            },
            {
                "title": "Separar alertas de bloqueos",
                "text": "No todos los problemas tienen la misma gravedad. La revision debe dejar claro que se puede aprobar con observaciones y que debe corregirse antes.",
            },
            {
                "title": "Cruzar la pieza con el entorno cuando haga falta",
                "text": "Si sospechas que el error depende del stack publicitario, completa el flujo revisando la pagina o el tag asociado.",
            },
        ],
        "primary_tool_slug": "creative-qa-checklist",
        "primary_tool_reason": "Creative QA Checklist ayuda a detectar justo esos errores repetidos: dimensiones invalidas, ausencia de click path, tracking incompleto, autoplay con sonido o peso excesivo.",
        "related_tool_slugs": ["creative-preview-lab", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Declara formato, dimensiones y destino",
                "text": "La salida mejora mucho cuando la herramienta entiende con claridad que tipo de pieza estas evaluando y hacia donde debe resolver.",
            },
            {
                "title": "Completa tracking, peso y comportamiento multimedia",
                "text": "Esos campos concentran varios de los errores que mas afectan aprobacion y delivery.",
            },
            {
                "title": "Lee el estado final de QA",
                "text": "La herramienta diferencia entre piezas listas, piezas con revision pendiente y piezas bloqueadas.",
            },
            {
                "title": "Abre preview si quieres validar el markup",
                "text": "Si el error parece venir del codigo o del tag, usa Creative Preview Lab para inspeccionar el render y los elementos detectados.",
            },
        ],
        "faqs": [
            {
                "question": "Cual es el error mas comun en una creatividad display?",
                "answer": "Depende del flujo, pero suelen repetirse ausencia de click path valido, tracking incompleto, peso excesivo y autoplay con sonido.",
            },
            {
                "question": "Una creatividad puede aprobar QA y fallar igual en serving?",
                "answer": "Si. El QA previo reduce errores, pero el serving final tambien depende del ad server, del entorno y de integraciones externas.",
            },
            {
                "question": "Conviene revisar el stack de la pagina si la pieza parece correcta?",
                "answer": "Si sospechas un problema de implementacion o monetizacion, si. No todos los errores se originan en la creatividad misma.",
            },
        ],
        "related_page_slugs": [
            "validar-creatividad-html",
            "preview-anuncios-html",
            "debug-gpt-ads",
        ],
    },
    {
        "slug": "como-validar-tags-publicitarios",
        "title": "Como validar tags publicitarios sin depender del ad server | Pi Development",
        "meta_description": "Guia tecnica para validar tags publicitarios y third-party tags: scripts, iframes, macros, click URL y limites del preview.",
        "meta_keywords": "validar tags publicitarios, third party tag, preview tag html, revisar tag de anuncios, macros publicitarias",
        "eyebrow": "Tags de terceros",
        "h1": "Como validar tags publicitarios y third-party tags",
        "description": "Los tags publicitarios suelen traer dependencias externas, macros y supuestos de entorno que conviene revisar antes de enviarlos a produccion.",
        "intro_paragraphs": [
            "Validar un tag publicitario exige distinguir entre lo que el snippet trae visible y lo que solo ocurrira cuando corra dentro del ad server o del entorno del vendor.",
            "Esa diferencia es importante porque muchos errores reales aparecen antes: scripts bloqueados, iframes inesperados, macros sin resolver, click URLs ambiguas o codigo que intenta escapar del contenedor.",
        ],
        "common_problems": [
            {
                "title": "El tag depende de macros o variables externas",
                "text": "Fuera del entorno propietario, esas macros no resuelven y el preview puede quedar parcial. Eso no invalida la revision, pero obliga a interpretarla bien.",
            },
            {
                "title": "Hay multiples scripts o iframes de terceros",
                "text": "Cuantas mas dependencias externas aparezcan, mas importante es documentar limitaciones, recursos cargados y posibles restricciones de sandbox.",
            },
            {
                "title": "No esta claro hacia donde resuelve el click",
                "text": "Un tag puede traer placeholders, click URL indirecta o comportamiento delegado. Sin esa lectura, es facil aprobar una pieza con el flujo de clic incompleto.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Renderizar el tag en un entorno contenido",
                "text": "Un sandbox controlado permite detectar scripts, iframes, enlaces y bloqueos sin comprometer el resto del sistema.",
            },
            {
                "title": "Cruzar preview con checklist tecnica",
                "text": "El render te muestra comportamiento visible; la checklist ayuda a ordenar aprobacion, tracking, peso y criterios de serving.",
            },
            {
                "title": "Revisar la pagina de destino si el problema apunta al entorno",
                "text": "Cuando el tag parece correcto pero el placement falla, conviene mirar la URL donde ese tag deberia convivir con el stack publicitario.",
            },
        ],
        "primary_tool_slug": "creative-preview-lab",
        "primary_tool_reason": "Creative Preview Lab permite pegar third-party tags en un sandbox controlado y devuelve hallazgos tecnicos sobre scripts, iframes, enlaces, macros y estado del render.",
        "related_tool_slugs": ["creative-qa-checklist", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Selecciona el modo third-party",
                "text": "Ese modo es el mas adecuado cuando el snippet depende de recursos o macros externas.",
            },
            {
                "title": "Pega el tag y define dimensiones",
                "text": "El tamano del contenedor ayuda a leer mejor si el problema es visual, estructural o de dependencias externas.",
            },
            {
                "title": "Inspecciona elementos detectados",
                "text": "La herramienta resume scripts, iframes, enlaces, recursos externos y macros visibles para que la revision sea menos ambigua.",
            },
            {
                "title": "Completa QA o debug de pagina si hace falta",
                "text": "Si el tag necesita aprobacion tecnica adicional o si el fallo parece del stack, continua con Creative QA Checklist o AdTech Debug Tool.",
            },
        ],
        "faqs": [
            {
                "question": "Un tag de terceros puede quedar parcial y aun asi estar bien?",
                "answer": "Si. Puede depender de macros, librerias o permisos que solo existen en el entorno real. Lo importante es documentar esa limitacion con claridad.",
            },
            {
                "question": "Conviene validar tags y creatividades con la misma herramienta?",
                "answer": "Conviene usar preview para el codigo o el tag, y una checklist para la aprobacion tecnica. Son capas complementarias.",
            },
            {
                "question": "Que hago si el tag intenta navegar fuera del frame?",
                "answer": "Eso es una senal importante. Un entorno controlado debe bloquear ese comportamiento y dejarlo visible como hallazgo tecnico.",
            },
        ],
        "related_page_slugs": [
            "preview-anuncios-html",
            "validar-creatividad-html",
            "debug-anuncios-web",
        ],
    },
    {
        "slug": "herramientas-adtech",
        "title": "Herramientas AdTech para QA tecnico, preview y diagnostico publicitario | Pi Development",
        "meta_description": "Hub tecnico de herramientas AdTech de Pi Development: diagnostico publicitario, validacion de creatividades, preview de anuncios HTML, QA tecnico publicitario, GPT y UTMs.",
        "meta_keywords": "herramientas adtech, validacion de creatividades, diagnostico tecnico publicitario, preview de anuncios html, qa tecnico publicitario, herramientas para google publisher tag",
        "eyebrow": "Suite tecnica",
        "h1": "Herramientas AdTech para diagnostico, QA y preview tecnico",
        "description": "Esta pagina concentra la suite tecnica de Pi Development para diagnostico publicitario, validacion de creatividades, preview de anuncios HTML, QA tecnico publicitario y control operativo de URLs.",
        "intro_paragraphs": [
            "Pi Development no presenta estas herramientas como una lista suelta. La suite esta organizada para responder problemas tecnicos concretos: detectar una implementacion con GPT, validar una creatividad antes de publicarla, probar un tag HTML, revisar una landing o construir UTMs limpias.",
            "La utilidad real aparece cuando eliges la herramienta segun la capa del problema. Si el fallo vive en la pagina monetizada, conviene empezar por diagnostico. Si esta en la creatividad o en el tag, entra por QA y preview. Si la duda esta en la URL final o en la landing, pasa a validacion tecnica y tracking.",
        ],
        "common_problems": [
            {
                "title": "Se mezclan problemas de pagina, creatividad y tracking",
                "text": "Cuando todo se diagnostica con el mismo criterio, es facil perder tiempo entre GPT, preview de tags, QA tecnico y revision de landing sin aislar el origen del fallo.",
            },
            {
                "title": "No hay un hub claro para repartir el flujo",
                "text": "Sin una URL central, la suite queda fragmentada: algunas personas llegan por una guia SEO, otras por una tool puntual, pero cuesta entender como se conecta el conjunto.",
            },
            {
                "title": "Se revisa demasiado tarde la capa tecnica basica",
                "text": "Muchas incidencias publicitarias se agravan porque no se valida a tiempo la creatividad, la landing o la URL etiquetada antes de entrar al serving o a campanas activas.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Separar el flujo por tipo de incidencia",
                "text": "Diagnostico publicitario para la pagina, QA y preview para creatividades, tracking para URLs y validacion tecnica para landing pages. Esa division evita lecturas ambiguas.",
            },
            {
                "title": "Usar la suite como un sistema de escalado",
                "text": "La primera lectura debe ayudarte a decidir el siguiente paso. Un debug de GPT puede derivar a preview de tag, y una validacion de landing puede derivar a UTMs o auditoria tecnica.",
            },
            {
                "title": "Documentar hallazgos con una hipotesis concreta",
                "text": "Cada herramienta esta pensada para cerrar con una accion util: corregir el markup, revisar la implementacion de GPT, ajustar la landing o reconstruir la URL final.",
            },
        ],
        "primary_tool_slug": "adtech-debug-tool",
        "primary_tool_reason": "AdTech Debug Tool es la mejor puerta de entrada cuando necesitas revisar monetizacion visible, senales de GPT, Google Publisher Tag, slots, wrappers o stack publicitario en una pagina.",
        "related_tool_slugs": ["creative-preview-lab", "creative-qa-checklist", "ai-auditor"],
        "how_to_use": [
            {
                "title": "Empieza por la categoria correcta",
                "text": "Si el problema esta en una pagina monetizada, entra por diagnostico. Si esta en una creatividad o un third-party tag, entra por QA y preview. Si la duda esta en la URL final, pasa a tracking.",
            },
            {
                "title": "Usa la tool principal como primera lectura",
                "text": "Cada bloque de esta pagina enlaza a la herramienta mas util para esa capa tecnica. Empieza por esa puerta y escala solo si la salida lo pide.",
            },
            {
                "title": "Cruza el resultado con guias relacionadas",
                "text": "Las guias SEO ayudan a entender cuando conviene usar preview de anuncios HTML, QA tecnico publicitario, herramientas para Google Publisher Tag o revision tecnica de landing.",
            },
            {
                "title": "Cierra con una accion operativa",
                "text": "La salida ideal no es una opinion general. Es una decision clara sobre que corregir, que validar despues y que herramienta usar a continuacion.",
            },
        ],
        "hub_use_cases": [
            {
                "title": "Validar una creatividad antes de publicarla",
                "text": "Empieza con Creative QA Checklist para revisar dimensiones, click path, tracking, autoplay y peso. Si necesitas ver el markup o un tag, continua con Creative Preview Lab.",
            },
            {
                "title": "Detectar problemas en una implementacion con GPT",
                "text": "Usa AdTech Debug Tool para confirmar senales visibles de GPT, wrappers, slots e iframes publicitarios. Si la incidencia parece del entorno, cruza la lectura con la guia de debug de GPT Ads.",
            },
            {
                "title": "Construir UTMs limpias para campanas",
                "text": "UTM Builder sirve para generar URLs consistentes sin romper query params existentes y dejar la URL final lista para compartir o validar.",
            },
            {
                "title": "Revisar una landing antes de campanas",
                "text": "AI Auditor y Landing Performance Snapshot ayudan a comprobar title, description, canonical, H1, respuesta inicial y otras senales tecnicas basicas antes de invertir trafico.",
            },
        ],
        "hub_sections": [
            {
                "cluster_key": "adtech",
                "title": "Diagnostico",
                "summary": "Este grupo sirve para revisar implementaciones publicitarias visibles, monetizacion, Google Publisher Tag y senales iniciales del stack en pagina.",
                "problem": "Conviene usarlo cuando necesitas detectar problemas de GPT, wrappers, slots, iframes, vendors o comportamiento publicitario visible antes de pasar a DevTools.",
                "use_case": "Es la mejor entrada para incidencias de monetizacion, debug tecnico publicitario y herramientas para Google Publisher Tag.",
            },
            {
                "cluster_key": "creatividades",
                "title": "QA y preview",
                "summary": "Este grupo concentra la validacion de creatividades, preview de anuncios HTML y lectura tecnica de tags o piezas antes de publicar.",
                "problem": "Resuelve dudas sobre dimensiones, click path, tracking, recursos externos, macros, autoplay y comportamiento de third-party tags.",
                "use_case": "Conviene usarlo cuando una creatividad necesita QA tecnico publicitario o cuando quieres revisar preview de anuncios HTML en un entorno controlado.",
            },
            {
                "cluster_key": "tracking",
                "title": "Tracking y operaciones",
                "summary": "Este bloque se centra en URLs operativas, etiquetado UTM y control de enlaces finales antes de activar trafico o compartir una landing.",
                "problem": "Ayuda a evitar UTMs rotas, nomenclaturas inconsistentes y errores manuales en la URL final que afectan medicion y trazabilidad.",
                "use_case": "Conviene usarlo cuando el problema no esta en la creatividad ni en GPT, sino en la construccion de la URL que va a circular en medios o reporting.",
            },
            {
                "cluster_key": "seo-performance",
                "title": "Rendimiento y validacion tecnica",
                "summary": "Este grupo sirve para revisar la base tecnica visible de una landing o URL publica antes de lanzar campanas o atribuir el problema a la capa publicitaria.",
                "problem": "Resuelve casos donde faltan metadatos, canonical, jerarquia HTML o una respuesta base consistente, y donde conviene validar el estado tecnico de la pagina.",
                "use_case": "Conviene usarlo cuando necesitas revisar una landing antes de campanas, validar SEO tecnico visible o confirmar que la URL final responde como esperas.",
            },
        ],
        "faqs": [
            {
                "question": "Que herramientas incluye esta pagina hub de Pi Development?",
                "answer": "Incluye herramientas para diagnostico publicitario, validacion de creatividades, preview de anuncios HTML, QA tecnico publicitario, auditoria tecnica de landing pages y construccion de UTMs.",
            },
            {
                "question": "Para quien sirve esta suite tecnica?",
                "answer": "Sirve para perfiles de AdOps, trafficking, QA tecnico, medios, monetizacion, growth y equipos que necesitan revisar una URL, una creatividad o una implementacion publicitaria con mas criterio tecnico.",
            },
            {
                "question": "Cuando conviene usar preview, QA o debug de pagina?",
                "answer": "Preview y QA convienen cuando el foco esta en la pieza o el tag. El debug de pagina conviene cuando el problema parece vivir en GPT, en la monetizacion visible o en la implementacion del sitio.",
            },
            {
                "question": "Estas herramientas reemplazan DevTools, GAM o QA manual?",
                "answer": "No. Funcionan como una capa de revision rapida y estructurada para llegar a la revision manual con una hipotesis tecnica mejor definida.",
            },
        ],
        "related_page_slugs": [
            "debug-anuncios-web",
            "debug-gpt-ads",
            "auditoria-tecnica-web",
            "como-crear-utms",
        ],
    },
]


def get_seo_page(slug):
    for page in SEO_PAGE_DEFINITIONS:
        if page["slug"] == slug:
            return deepcopy(page)
    return None


def get_public_seo_page_slugs():
    return [page["slug"] for page in SEO_PAGE_DEFINITIONS]


def get_related_seo_pages(slugs):
    pages = []
    for slug in slugs:
        page = get_seo_page(slug)
        if page:
            pages.append(page)
    return pages
