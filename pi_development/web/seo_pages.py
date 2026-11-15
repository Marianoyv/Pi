from copy import deepcopy


SEO_PAGE_DEFINITIONS = [
    {
        "slug": "validar-creatividad-html",
        "title": "How to validate an HTML creative before trafficking | Pi Development",
        "meta_description": "Technical guide to validate an HTML creative: dimensions, clickTag, tracking, weight, autoplay and dependencies before approving a piece.",
        "meta_keywords": "validate html creativity, qa html creativity, review html5 banner, clicktag, advertising tracking",
        "eyebrow": "Creative QA",
        "h1": "How to validate an HTML creative before trafficking",
        "description": "This page summarizes the technical controls that should be done on an HTML creative before sending it to trafficking or uploading it to a platform.",
        "intro_paragraphs": [
            "Validating an HTML creative is not just about opening the file and checking that it is visible. In a technical review it is advisable to review dimensions, clickTag, external dependencies, weight, multimedia behavior and tracking traces.",
            "When this validation is omitted, errors appear in serving: pieces that do not load, clicks that do not resolve, incomplete measurement or behaviors that violate autoplay policies. The idea of ​​this guide is to order that first pass with useful criteria.",
        ],
        "common_problems": [
            {
                "title": "Incomplete or ambiguous click path",
                "text": "The piece declares a link, but it is not clear if it uses clickTag, platform macro or a hardcoded URL that can break the serving flow.",
            },
            {
                "title": "Markup dependent on external resources",
                "text": "Scripts, fonts, videos or remote images can block the render or alter the final behavior if the serving environment does not replicate the development environment.",
            },
            {
                "title": "Autoplay, weight or dimensions out of criteria",
                "text": "A creative can look correct and still fail due to excessive weight, audio when loading or dimensions that do not match the intended placement.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Separate structure review and serving review",
                "text": "First validate the piece itself: dimensions, click path, weight and dependencies. Then check the context where it is going to be delivered.",
            },
            {
                "title": "Use a checklist before approving",
                "text": "A checklist avoids overlooking repeated errors such as no tracking, broken destination or unauthorized audio configurations.",
            },
            {
                "title": "Open a controlled preview when there is HTML or tags",
                "text": "If the asset includes scripts or third parties, controlled preview helps distinguish between a code problem and an environment limitation.",
            },
        ],
        "primary_tool_slug": "creative-qa-checklist",
        "primary_tool_reason": "Creative QA Checklist orders the initial validation of the piece and flags real alerts about click path, tracking, weight, autoplay and serving context.",
        "related_tool_slugs": ["creative-preview-lab", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Load the base data of the part",
                "text": "Complete name, format, dimensions, destination URL, presence of click path and declared weight.",
            },
            {
                "title": "Mark multimedia behavior and context",
                "text": "Indicates autoplay, sound, target device and whether the creative will run in SafeFrame, iframe or a still uncertain context.",
            },
            {
                "title": "Check alerts and blocking points",
                "text": "The tool separates minor observations from blockages that should be corrected before approving the creative.",
            },
            {
                "title": "Go to a preview if you need to see the markup",
                "text": "If you also want to inspect visible scripts, iframes or macros, open Creative Preview Lab as a second step.",
            },
        ],
        "faqs": [
            {
                "question": "What is the difference between validating and previewing an HTML creative?",
                "answer": "Validating involves reviewing technical and approval criteria. The preview is used to see how the markup responds within a controlled environment. The normal thing is to use both steps when the part has a code.",
            },
            {
                "question": "Can a creative be validated without having the final ZIP?",
                "answer": "Yeah. A first pass can be done with manual data, as long as you declare dimensions, destination, tracking and multimedia behavior accurately.",
            },
            {
                "question": "This guide replaces the final trafficking QA?",
                "answer": "No. It mandates pre-validation, but the final QA still depends on the ad server, the platform, and the actual delivery environment.",
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
        "title": "Preview HTML ads in a controlled environment | Pi Development",
        "meta_description": "How to preview HTML ads and third-party tags without depending on the ad server: iframe sandbox, scripts, iframes, macros and real limits.",
        "meta_keywords": "preview html ads, preview html banner, preview advertising tag, html sandbox, rich media preview",
        "eyebrow": "Technical view",
        "h1": "HTML and rich media ad preview",
        "description": "If you need to review advertising markup before integrating it, this guide explains that it is best to look at a controlled preview and that you should not assume.",
        "intro_paragraphs": [
            "An HTML ad preview serves to answer a specific question: does the code render readably within a controlled container or does it already expose visible problems on the first load?",
            "That is not equivalent to replicating SafeFrame, an ad server or all the events of a real environment. The usefulness of the preview is to detect scripts, iframes, links, macros or immediate blocks before escalating to a more expensive revision.",
        ],
        "common_problems": [
            {
                "title": "The part only works within a proprietary environment",
                "text": "Many tags depend on variables, macros or permissions that do not exist in a generic preview, so the render may be partial or empty.",
            },
            {
                "title": "External scripts or iframes are blocked",
                "text": "The browser may restrict third-party resources, and this makes visible a technical limitation that should be documented before approving the piece.",
            },
            {
                "title": "It is assumed that the preview replicates the actual serving",
                "text": "A controlled preview helps inspect markup, but does not guarantee clicks, measurement, refresh or the exact behavior of the ad stack.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Define dimensions and input mode before rendering",
                "text": "Technical reading improves if the piece enters with a clear size and if you distinguish between your own HTML and third-party tags.",
            },
            {
                "title": "Read the preview along with the detected elements",
                "text": "It is not enough to look if you see something. It is worth checking how many scripts, iframes, links, macros or external resources appear in the code.",
            },
            {
                "title": "Escalate to QA or debug depending on the problem",
                "text": "If the problem is with the part, go to a QA checklist. If you suspect an ad stack limitation, check the page with an AdTech tool.",
            },
        ],
        "primary_tool_slug": "creative-preview-lab",
        "primary_tool_reason": "Creative Preview Lab allows you to paste HTML or advertising tags, render a sandbox preview and receive immediate technical findings on scripts, iframes, links and macros.",
        "related_tool_slugs": ["creative-qa-checklist", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Select type of part and dimensions",
                "text": "Declare whether you are testing display, rich media, or third-party tag, and define width and height for the container.",
            },
            {
                "title": "Paste the markup or tag",
                "text": "Use HTML if you control the code or third-party mode if you are reviewing a snippet delivered by a vendor.",
            },
            {
                "title": "Read render status",
                "text": "The output tells you whether the preview was successful, partial, locked, or empty. This distinction avoids misinterpreting the result.",
            },
            {
                "title": "Review limitations and decide the next step",
                "text": "If the preview is partial due to external dependencies, document it and complete the review with technical QA or environment debugging.",
            },
        ],
        "faqs": [
            {
                "question": "Does a correct preview mean that the piece is ready to serve?",
                "answer": "Not necessarily. It means that the markup was rendered inside the sandbox. Serving, tracking, clicks and compatibility still need to be validated in the real environment.",
            },
            {
                "question": "Why do some tags remain blank?",
                "answer": "Because they depend on external resources, macros or permissions that do not exist outside of the proprietary environment where they normally run.",
            },
            {
                "question": "Is it convenient to use preview and checklist together?",
                "answer": "Yeah. The preview shows the visual behavior and the checklist orders the technical approval of the part.",
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
        "title": "How to debug web ads and visible advertising stack | Pi Development",
        "meta_description": "Guide to debug web ads: GPT signals, Prebid, wrappers, slots, iframes and readings visible from the backend.",
        "meta_keywords": "debug web ads, advertising diagnosis, check gpt, prebid debug, advertising stack",
        "eyebrow": "Diagnostico AdTech",
        "h1": "How to debug web ads and visible advertising implementation",
        "description": "When a monetized page does not behave as you expect, it is advisable to separate advertising stack problems, markup problems and real serving problems.",
        "intro_paragraphs": [
            "Debugging web ads involves identifying which signals from the ad stack are actually visible on the page and which only appear while the browser is running.",
            "The first useful reading usually relies on the initial HTML: GPT or Prebid scripts, known wrappers, iframes, slot hints and other patterns that help you know where to start the review.",
        ],
        "common_problems": [
            {
                "title": "It is not clear if the page loads GPT, Prebid or both",
                "text": "In mixed implementations it is easy to waste time looking in the wrong place if you don't first confirm which libraries appear in the initial response.",
            },
            {
                "title": "Slots are not readable in the HTML",
                "text": "There may be visible advertising scripts, but without a clear structure of containers or identifiers that help map placements.",
            },
            {
                "title": "Part of the stack only exists on the client side",
                "text": "If a large part of the implementation is mounted in runtime, a backend read is enough to detect signs, not to confirm complete serving.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Start with the initial answer",
                "text": "First confirm if any scripts, vendors, wrappers, iframes or monetization patterns appear before going into a deeper manual inspection.",
            },
            {
                "title": "Separate visible signs of hypotheses",
                "text": "The important thing is not to guess the entire stack, but to clearly document which components were seen and which part remains uncertain.",
            },
            {
                "title": "Cross the discovery with the piece when necessary",
                "text": "If the page loads an ad stack but the creative fails, the next step is usually to review the piece or tag in parallel.",
            },
        ],
        "primary_tool_slug": "adtech-debug-tool",
        "primary_tool_reason": "AdTech Debug Tool inspects a public URL and detects visible signals from GPT, Google Ad Manager, Prebid, known vendors, slots and advertising iframes.",
        "related_tool_slugs": ["ai-auditor", "creative-preview-lab"],
        "how_to_use": [
            {
                "title": "Load the URL of the page with ads",
                "text": "Use a public URL that exposes the initial HTML of the placement or monetized page you want to review.",
            },
            {
                "title": "Read the detected signals",
                "text": "The tool lists patterns compatible with GPT, Prebid, AdSense, wrappers and other signals visible from the backend.",
            },
            {
                "title": "Review findings and limitations",
                "text": "When the reading is partial, the output makes it clear. This avoids drawing too strong conclusions from incomplete HTML.",
            },
            {
                "title": "Go to preview or QA if the problem points to the part",
                "text": "If the stack appears present but the creative is not responding, complete the review with Creative Preview Lab or Creative QA Checklist.",
            },
        ],
        "faqs": [
            {
                "question": "Does the tool confirm the actual serving of the ads?",
                "answer": "No. Confirm visible signs in the initial response. The actual serving and network requests still need a browser overhaul.",
            },
            {
                "question": "Can you detect Prebid even if the page renders a lot with JavaScript?",
                "answer": "If the library or its patterns appear in the downloaded HTML, yes. If everything is mounted client-side, the read may be partial.",
            },
            {
                "question": "When is it appropriate to combine page debug and tag preview?",
                "answer": "When the problem can come from both the advertising environment and the creative code or the third-party tag.",
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
        "meta_description": "How to review visible signals from Google Publisher Tag, Google Ad Manager, slots and advertising iframes in a public URL.",
        "meta_keywords": "debug gpt ads, google publisher tag, google ad manager debug, revisar slots gpt, anuncios gpt",
        "eyebrow": "Google Publisher Tag",
        "h1": "How to debug GPT Ads on a web page",
        "description": "This guide focuses on a specific question: the page displays visible signals compatible with Google Publisher Tag and a minimum structure of advertising slots.",
        "intro_paragraphs": [
            "When talking about GPT Ads debugging, three different layers are often mixed: presence of the GPT library, slot configuration and effective serving from Google Ad Manager.",
            "A first technical reading does not replace DevTools, but it serves to detect if the page already exposes GPT scripts, advertising iframes or patterns that justify delving deeper into that stack.",
        ],
        "common_problems": [
            {
                "title": "GPT is loaded but the slots are not evident",
                "text": "The GPT library can appear and still not be clear where the containers are defined or how the visible inventory is organized.",
            },
            {
                "title": "The page mixes GPT with wrappers or header bidding",
                "text": "When several advertising layers coexist, it is advisable to first confirm what is seen in the initial response so as not to confuse responsibilities.",
            },
            {
                "title": "Backend detection is partial",
                "text": "If a large part of the stack is built with JavaScript, the backend analysis can hint at GPT, but not always describe the entire loading sequence.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Confirm presence of the GPT library",
                "text": "First look for routes, scripts or googletag patterns compatible with the Google Publisher Tag.",
            },
            {
                "title": "Review evidence of slots and iframes",
                "text": "If the page exposes containers, slot hints or advertising iframes, you already have a better basis to inspect the inventory.",
            },
            {
                "title": "Escalate to manual review only with a clear hypothesis",
                "text": "The initial reading should help you decide if the next step is in GAM, in header bidding, in the creative or in the browser runtime.",
            },
        ],
        "primary_tool_slug": "adtech-debug-tool",
        "primary_tool_reason": "AdTech Debug Tool is the best entry to check if a URL exposes visible signals from GPT, Google Ad Manager, slots and advertising iframes.",
        "related_tool_slugs": ["creative-preview-lab", "ai-auditor"],
        "how_to_use": [
            {
                "title": "Paste the URL where GPT should run",
                "text": "Use the exact page where the placement or monetization is raising doubts.",
            },
            {
                "title": "Find GPT and Google Ad Manager matches",
                "text": "The output shows you detected scripts and patterns that point to the visible presence of GPT.",
            },
            {
                "title": "Check if there are visible slots or iframes",
                "text": "This helps you distinguish between a clear stack loading and a configuration that is too opaque in the initial response.",
            },
            {
                "title": "Document the visible and the uncertain",
                "text": "If the tool indicates render limitations, use that information to better frame a later manual review.",
            },
        ],
        "faqs": [
            {
                "question": "Detecting GPT means that Google Ad Manager is serving well?",
                "answer": "No. It means that there are visible signals compatible with GPT. The actual serving requires confirming requests, slots and response from the ad server in the browser.",
            },
            {
                "question": "Does it work for pages with header bidding?",
                "answer": "Yeah. The read can show GPT and at the same time wrappers or bidding libraries if they appear in the initial HTML.",
            },
            {
                "question": "What do I do if the tool does not detect GPT but I suspect it exists?",
                "answer": "The implementation will likely be loaded on the client side or in another layer. The tool then serves as a signal of limitation, not as proof of absence.",
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
        "title": "How to create UTMs without breaking the destination URL | Pi Development",
        "meta_description": "Guide to creating UTM parameters with technical criteria: source, medium, campaign, query params preservation and naming control.",
        "meta_keywords": "how to create utms, generate utm, utm parameters, url tracking, campaign tagging",
        "eyebrow": "Tracking and operation",
        "h1": "How to create UTMs without breaking the destination URL",
        "description": "UTM parameters seem simple, but in teams with multiple hands they often break due to inconsistent naming, overwriting of queries or copying errors.",
        "intro_paragraphs": [
            "Creating UTMs is not just about concatenating key-value pairs to the end of a URL. It is advisable to preserve existing queries, normalize names and avoid ambiguous values ​​that later make the analytical reading useless.",
            "This guide aims at a sober operational flow: build the final URL, check that the base parameters are present and check that the destination landing page is still correct after tagging.",
        ],
        "common_problems": [
            {
                "title": "If you step on existing query params",
                "text": "It is common to lose important product, language or referrer parameters when the URL is reconstructed manually and without control.",
            },
            {
                "title": "Each person names a different source and campaign",
                "text": "The problem is not technical but operational: the taxonomy becomes inconsistent and then it is difficult to read campaigns or compare results.",
            },
            {
                "title": "The final URL is malformed",
                "text": "Spaces, capital letters, empty values ​​or duplication of UTMs often end in incorrect links or unreliable measurement.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Always start from the final destination URL",
                "text": "Before adding UTMs, confirm that the correct landing page is already responsive and that the base URL does not need additional adjustments.",
            },
            {
                "title": "Complete only the fields that have a clear convention",
                "text": "source, medium and campaign are usually required. term and content should be used only when they provide real reading.",
            },
            {
                "title": "Review tagged URL before sharing",
                "text": "Quick validation prevents publishing links with broken queries or inconsistent nomenclature.",
            },
        ],
        "primary_tool_slug": "utm-builder",
        "primary_tool_reason": "UTM Builder safely rebuilds the URL, preserves existing query params, and flags missing base fields such as source, medium, or campaign.",
        "related_tool_slugs": ["landing-performance-snapshot", "ai-auditor"],
        "how_to_use": [
            {
                "title": "Paste the destination URL",
                "text": "Use the final landing you want to measure. If you already have query params, the tool preserves them.",
            },
            {
                "title": "Completa source, medium y campaign",
                "text": "These three fields are usually the minimum useful to maintain analytical consistency.",
            },
            {
                "title": "Add term or content only if they provide reading",
                "text": "It is not advisable to fill out optional fields out of inertia. Better to use them when they differentiate creativity, keyword or variant.",
            },
            {
                "title": "Copy the final URL and validate the landing",
                "text": "If you want a second technical verification, you can pass the URL tagged by Landing Performance Snapshot or AI Auditor.",
            },
        ],
        "faqs": [
            {
                "question": "Does the tool remove parameters that were already in the URL?",
                "answer": "No. It preserves existing query params and only overwrites a key if you send a UTM with that same name.",
            },
            {
                "question": "Is it appropriate to put capital letters or spaces in UTMs?",
                "answer": "The usual thing is to normalize to consistent and readable values. Avoiding spaces and arbitrary changes helps sustain the taxonomy.",
            },
            {
                "question": "After creating UTMs, should you review the landing page?",
                "answer": "Yes, especially when the destination URL is already complex or when the campaign depends on a landing page with delicate technical rules.",
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
        "title": "Technical web audit to detect visible problems | Pi Development",
        "meta_description": "How to do a first-pass technical web audit: HTTP status, response, metadata, HTML structure and opportunities for improvement.",
        "meta_keywords": "web technical auditoria, web technical analyses, url review, web diagnostics, basic technical SEO",
        "eyebrow": "Web diagnostic",
        "h1": "First pass technical web audit",
        "description": "An initial technical web audit serves to sort out priorities before entering into a deeper review of performance, SEO or monetization.",
        "intro_paragraphs": [
            "In a first pass, it is advisable to review what can really be read from a public URL: HTTP status, response time, central metadata, basic HTML structure and some indications of technical quality.",
            "This type of audit does not replace crawling, multi-page analysis or a browser review, but it allows us to detect obvious gaps and define where to continue working.",
        ],
        "common_problems": [
            {
                "title": "The URL is responsive, but the technical basis is not clear",
                "text": "It is common to find pages published with a useless title, missing meta description, missing canonical or a confusing HTML hierarchy.",
            },
            {
                "title": "There is no useful prioritization of findings",
                "text": "Without an orderly read, teams end up mixing minor observations with problems that actually affect indexing or base experience.",
            },
            {
                "title": "The review is too manual",
                "text": "Opening several tools to confirm the basics consumes time and makes it more difficult to maintain a constant operational check.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Read the initial HTTP and HTML response first",
                "text": "With that base you can now detect redirects, missing metadata, missing canonical or multiple H1s without going into a heavier analysis yet.",
            },
            {
                "title": "Separate observations from opportunities",
                "text": "A good diagnosis not only lists problems: it also orders priorities and recommended next steps.",
            },
            {
                "title": "Combine extensive auditing with snapshots when necessary",
                "text": "If you only need a quick check of metadata or structure, a short snapshot can complement the main audit very well.",
            },
        ],
        "primary_tool_slug": "ai-auditor",
        "primary_tool_reason": "AI Auditor organizes a short technical reading on general status, observations, basic SEO, performance and opportunities for a public URL.",
        "related_tool_slugs": ["landing-performance-snapshot", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Load the public URL",
                "text": "Start with the real page you want to review, not a mock or partial development path.",
            },
            {
                "title": "Read the general condition and technical observations",
                "text": "The tool structures the output so that you distinguish general health, technical findings and opportunities.",
            },
            {
                "title": "Review basic SEO and performance",
                "text": "If there are missing title, meta description, canonical or response problems, they are visible in the same reading.",
            },
            {
                "title": "Go deeper according to the type of discovery",
                "text": "If the problem is simple metadata, use Landing Performance Snapshot. If there are monetization questions, open AdTech Debug Tool.",
            },
        ],
        "faqs": [
            {
                "question": "Is this audit valid for the entire site?",
                "answer": "No. It is used for the URL you send and as a starting point to define priorities. A complete site requires another depth.",
            },
            {
                "question": "Does it include technical SEO?",
                "answer": "It includes a basic and technical SEO reading on the analyzed URL, focusing on title, description, canonical, robots and initial HTML structure.",
            },
            {
                "question": "When is it appropriate to use a snapshot instead of a technical audit?",
                "answer": "When you only need a quick check of status, metadata and basic structure, without a broader reading of opportunities.",
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
        "title": "How to analyze the SEO of a page from the initial response | Pi Development",
        "meta_description": "Guide to analyze on-page and basic technical SEO: title, meta description, canonical, robots, H1 and visible HTML structure.",
        "meta_keywords": "analyze seo page, seo on page technical, title meta description canonical, review seo url",
        "eyebrow": "basic SEO",
        "h1": "How to analyze the SEO of a website",
        "description": "Analyzing the SEO of a page does not always require complete crawling. Many useful signals can be detected in the initial URL response.",
        "intro_paragraphs": [
            "For a first SEO review, it is advisable to observe basic but decisive elements: title, meta description, canonical, robots and the main hierarchy of the HTML that the user or crawler receives.",
            "Not all technical SEO ends there, but that initial reading is enough to find obvious gaps, duplications or configurations that affect indexing and semantic clarity.",
        ],
        "common_problems": [
            {
                "title": "Title and description absent or weak",
                "text": "Without these elements, the page loses clarity for search engines and is less prepared to capture queries with a specific intention.",
            },
            {
                "title": "Canonical or poorly solved robots",
                "text": "A missing canonical or a poorly applied restrictive directive can raise indexing questions even on technically simple pages.",
            },
            {
                "title": "Messy HTML hierarchy",
                "text": "Multiple H1s or an unfocused structure are often an early sign of content architecture problems.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Start with a URL and a specific reading",
                "text": "Before looking at huge suites, it is worth confirming whether the page already resolves its metadata and its main structure well.",
            },
            {
                "title": "Prioritize missing items that impact indexing",
                "text": "Title, description, canonical, robots and H1 usually give a first list of tasks that is much more useful than an unordered enumeration.",
            },
            {
                "title": "Cross basic SEO with technical status",
                "text": "If the response is slow, there are strange redirects or the page loads poorly, on-page SEO should not be analyzed in isolation from the technical base.",
            },
        ],
        "primary_tool_slug": "ai-auditor",
        "primary_tool_reason": "AI Auditor combines technical reading and basic SEO for a public URL, with organized findings and a clear next step recommendation.",
        "related_tool_slugs": ["landing-performance-snapshot", "utm-builder"],
        "how_to_use": [
            {
                "title": "Load the URL you want to review",
                "text": "Use the specific page you want to position or diagnose, not a generic homepage if the problem lives on a specific URL.",
            },
            {
                "title": "Revisa title, description, canonical y robots",
                "text": "These four fields usually explain a large part of the technical SEO problems visible on a first pass.",
            },
            {
                "title": "Check the basic HTML structure",
                "text": "Counting H1s and reading the initial HTML help detect a weak or inconsistent editorial hierarchy.",
            },
            {
                "title": "If you need a shorter reading, use the snapshot",
                "text": "Landing Performance Snapshot is useful when you only want to check metadata and structure without going through a broader audit.",
            },
        ],
        "faqs": [
            {
                "question": "Is analyzing the SEO of a page the same as doing a complete audit?",
                "answer": "No. This guide covers an initial and on-page reading. A complete audit requires more context, more URLs and other layers of analysis.",
            },
            {
                "question": "Is it advisable to review SEO even if the page is already indexed?",
                "answer": "Yeah. An indexed page may still have weak metadata, missing canonical, or unclear HTML structure.",
            },
            {
                "question": "Do UTMs affect this analysis?",
                "answer": "They can affect the operational reading of shared URLs. That is why it makes sense to review the labeling and final version of the landing page when they are part of the flow.",
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
        "title": "Frequent errors in display creatives and how to detect them | Pi Development",
        "meta_description": "Common errors in display creatives: dimensions, click path, tracking, autoplay, weight, external resources and serving context.",
        "meta_keywords": "errores creatividades display, qa banners, problemas html5 ads, clicktag, autoplay creative",
        "eyebrow": "Common problems",
        "h1": "Common errors in display creatives",
        "description": "A large part of the rejections or failures in display campaigns are explained by a fairly repeatable set of technical errors prior to trafficking.",
        "intro_paragraphs": [
            "In display creatives the problem is not always spectacular. These are often predictable technical details: incorrectly declared dimensions, dubious click path, incomplete tracking, excessive weight or out-of-policy autoplay.",
            "That is why it is advisable to work with a short but consistent review that allows you to block what is important before the piece reaches serving, final QA or publication.",
        ],
        "common_problems": [
            {
                "title": "Dimensions and format do not match the placement",
                "text": "A creative can look good separately and still be useless if it does not respect the inventory or the format where it will be served.",
            },
            {
                "title": "Tracking o click path sin validar",
                "text": "Absence of clickTag, poorly resolved macros or unchecked destination URL are very common operational errors.",
            },
            {
                "title": "Heavy resources or blocking behavior",
                "text": "High weight, autoplay with sound or fragile external dependencies usually turn into technical rejection or bad charging experience.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Apply a checklist before the preview",
                "text": "First it is advisable to sort the approval criteria and then look at the render of the piece. This way you prevent a correct preview from covering up a policy or tracking problem.",
            },
            {
                "title": "Separate crash alerts",
                "text": "Not all problems have the same severity. The review should make it clear that it can be approved with comments and that it must be corrected first.",
            },
            {
                "title": "Cross the piece with the environment when necessary",
                "text": "If you suspect that the error depends on the advertising stack, complete the flow by reviewing the page or the associated tag.",
            },
        ],
        "primary_tool_slug": "creative-qa-checklist",
        "primary_tool_reason": "Creative QA Checklist helps detect just those repeated errors: invalid dimensions, absence of click path, incomplete tracking, autoplay with sound or excessive weight.",
        "related_tool_slugs": ["creative-preview-lab", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Declare format, dimensions and destination",
                "text": "The output improves greatly when the tool clearly understands what type of part you are evaluating and where it should resolve.",
            },
            {
                "title": "Complete tracking, weight and multimedia behavior",
                "text": "These fields concentrate several of the errors that most affect approval and delivery.",
            },
            {
                "title": "Read the final QA status",
                "text": "The tool differentiates between ready parts, parts with pending review and blocked parts.",
            },
            {
                "title": "Open preview if you want to validate the markup",
                "text": "If the error seems to come from the code or the tag, use Creative Preview Lab to inspect the render and the detected elements.",
            },
        ],
        "faqs": [
            {
                "question": "What is the most common mistake in a creative display?",
                "answer": "It depends on the flow, but absence of a valid click path, incomplete tracking, excessive weight and autoplay with sound are usually repeated.",
            },
            {
                "question": "Can a creative pass QA and still fail in serving?",
                "answer": "Yeah. Previous QA reduces errors, but the final serving also depends on the ad server, the environment and external integrations.",
            },
            {
                "question": "Is it advisable to check the page stack if the part seems correct?",
                "answer": "If you suspect an implementation or monetization problem, yes. Not all mistakes originate in creativity itself.",
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
        "title": "How to validate advertising tags without depending on the ad server | Pi Development",
        "meta_description": "Technical guide to validate advertising tags and third-party tags: scripts, iframes, macros, click URL and preview limits.",
        "meta_keywords": "validate advertising tags, third party tag, preview html tag, review advertising tag, advertising macros",
        "eyebrow": "Third party tags",
        "h1": "How to validate advertising tags and third-party tags",
        "description": "Advertising tags usually come with external dependencies, macros and environmental assumptions that should be reviewed before sending them to production.",
        "intro_paragraphs": [
            "Validating an advertising tag requires distinguishing between what the snippet is visible and what will only occur when it runs within the ad server or the vendor's environment.",
            "That difference is important because many real errors appear earlier: blocked scripts, unexpected iframes, unresolved macros, ambiguous click URLs, or code that tries to escape the container.",
        ],
        "common_problems": [
            {
                "title": "The tag depends on macros or external variables",
                "text": "Outside the proprietary environment, these macros do not resolve and the preview may remain partial. That does not invalidate the review, but it requires it to be interpreted correctly.",
            },
            {
                "title": "There are multiple third-party scripts or iframes",
                "text": "The more external dependencies that appear, the more important it is to document limitations, loaded resources, and possible sandbox restrictions.",
            },
            {
                "title": "It is not clear where the click resolves",
                "text": "A tag can bring placeholders, indirect URL clicks or delegated behavior. Without that reading, it's easy to approve a piece with an incomplete click flow.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Render the tag in a contained environment",
                "text": "A controlled sandbox allows you to detect scripts, iframes, links and crashes without compromising the rest of the system.",
            },
            {
                "title": "Cross preview with technical checklist",
                "text": "The render shows you visible behavior; The checklist helps to sort approval, tracking, weight and serving criteria.",
            },
            {
                "title": "Review the landing page if the problem points to the environment",
                "text": "When the tag seems correct but the placement fails, it is advisable to look at the URL where that tag should coexist with the advertising stack.",
            },
        ],
        "primary_tool_slug": "creative-preview-lab",
        "primary_tool_reason": "Creative Preview Lab allows you to paste third-party tags into a controlled sandbox and returns technical findings about scripts, iframes, links, macros and render status.",
        "related_tool_slugs": ["creative-qa-checklist", "adtech-debug-tool"],
        "how_to_use": [
            {
                "title": "Select third-party mode",
                "text": "This mode is the most appropriate when the snippet depends on external resources or macros.",
            },
            {
                "title": "Paste the tag and define dimensions",
                "text": "The size of the container helps to better read if the problem is visual, structural or external dependencies.",
            },
            {
                "title": "Inspect detected items",
                "text": "The tool summarizes visible scripts, iframes, links, external resources, and macros to make the review less ambiguous.",
            },
            {
                "title": "Complete QA or page debug if necessary",
                "text": "If the tag requires additional technical approval or if the bug appears to be stack-specific, continue with the Creative QA Checklist or AdTech Debug Tool.",
            },
        ],
        "faqs": [
            {
                "question": "Can a third-party tag be partial and still be fine?",
                "answer": "Yeah. It may depend on macros, libraries or permissions that only exist in the real environment. The important thing is to document that limitation clearly.",
            },
            {
                "question": "Is it convenient to validate tags and creatives with the same tool?",
                "answer": "It is advisable to use a preview for the code or tag, and a checklist for technical approval. They are complementary layers.",
            },
            {
                "question": "What do I do if the tag tries to navigate outside the frame?",
                "answer": "That is an important sign. A controlled environment should block that behavior and leave it visible as a technical finding.",
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
        "title": "AdTech tools for technical QA, preview and advertising diagnosis | Pi Development",
        "meta_description": "Pi Development's AdTech tools technical hub: advertising diagnosis, creative validation, HTML ad preview, advertising technical QA, GPT and UTMs.",
        "meta_keywords": "adtech tools, creative validation, advertising technical diagnosis, html ad preview, advertising technical qa, tools for google publisher tag",
        "eyebrow": "Technical suite",
        "h1": "AdTech tools for diagnosis, QA and technical preview",
        "description": "This page concentrates the Pi Development technical suite for advertising diagnosis, creative validation, HTML ad preview, advertising technical QA and operational control of URLs.",
        "intro_paragraphs": [
            "Pi Development does not present these tools as a loose list. The suite is organized to answer specific technical problems: detect an implementation with GPT, validate a creative before publishing it, test an HTML tag, review a landing or build clean UTMs.",
            "The real usefulness appears when you choose the tool according to the layer of the problem. If the fault lives on the monetized page, it is advisable to start with a diagnosis. If it is in the creative or in the tag, enter through QA and preview. If the doubt is in the final URL or in the landing, go to technical validation and tracking.",
        ],
        "common_problems": [
            {
                "title": "Page, creativity and tracking problems are mixed",
                "text": "When everything is diagnosed with the same criteria, it is easy to waste time between GPT, tag preview, technical QA and landing review without isolating the source of the failure.",
            },
            {
                "title": "There is no clear hub to distribute the flow",
                "text": "Without a central URL, the suite is fragmented: some people come for an SEO guide, others for a specific tool, but it is difficult to understand how the whole thing is connected.",
            },
            {
                "title": "The basic technical layer is reviewed too late",
                "text": "Many advertising incidents are aggravated because the creative, the landing or the tagged URL is not validated in time before entering the serving or active campaigns.",
            },
        ],
        "recommended_approach": [
            {
                "title": "Separate the flow by type of incident",
                "text": "Advertising diagnosis for the page, QA and preview for creatives, tracking for URLs and technical validation for landing pages. This division avoids ambiguous readings.",
            },
            {
                "title": "Use the suite as a scaling system",
                "text": "The first reading should help you decide the next step. A GPT debug can lead to a tag preview, and a landing validation can lead to UTMs or technical audit.",
            },
            {
                "title": "Document findings with a specific hypothesis",
                "text": "Each tool is designed to close with a useful action: correct the markup, review the GPT implementation, adjust the landing or reconstruct the final URL.",
            },
        ],
        "primary_tool_slug": "adtech-debug-tool",
        "primary_tool_reason": "AdTech Debug Tool is the best gateway when you need to check visible monetization, GPT signals, Google Publisher Tag, slots, wrappers or advertising stack on a page.",
        "related_tool_slugs": ["creative-preview-lab", "creative-qa-checklist", "ai-auditor"],
        "how_to_use": [
            {
                "title": "Start with the correct category",
                "text": "If the problem is on a monetized page, enter it for diagnosis. If it is in a creative or a third-party tag, enter through QA and preview. If the doubt is in the final URL, go to tracking.",
            },
            {
                "title": "Use the main tool as the first reading",
                "text": "Each block on this page links to the most useful tool for that technical layer. Start with that door and climb only if the exit asks for it.",
            },
            {
                "title": "Cross the result with related guides",
                "text": "SEO guides help you understand when it is appropriate to use HTML ad previews, technical advertising QA, tools for Google Publisher Tag or technical landing review.",
            },
            {
                "title": "Close with an operational action",
                "text": "The ideal output is not a general opinion. It's a clear decision about what to fix, what to validate next, and what tool to use next.",
            },
        ],
        "hub_use_cases": [
            {
                "title": "Validate a creative before publishing it",
                "text": "Get started with the Creative QA Checklist to review dimensions, click path, tracking, autoplay, and weight. If you need to see the markup or a tag, continue with Creative Preview Lab.",
            },
            {
                "title": "Detect problems in an implementation with GPT",
                "text": "Use AdTech Debug Tool to confirm visible GPT signals, wrappers, slots and advertising iframes. If the issue seems to be from the environment, read the GPT Ads debug guide.",
            },
            {
                "title": "Build clean UTMs for campaigns",
                "text": "UTM Builder is used to generate consistent URLs without breaking existing query params and leaving the final URL ready to share or validate.",
            },
            {
                "title": "Review a landing before campaigns",
                "text": "AI Auditor and Landing Performance Snapshot help check title, description, canonical, H1, initial response and other basic technical signals before investing traffic.",
            },
        ],
        "hub_sections": [
            {
                "cluster_key": "adtech",
                "title": "Diagnostics",
                "summary": "This group is used to review visible advertising implementations, monetization, Google Publisher Tag and initial signals of the on-page stack.",
                "problem": "It is convenient to use it when you need to detect problems with GPT, wrappers, slots, iframes, vendors or visible advertising behavior before moving to DevTools.",
                "use_case": "It is the best entry for monetization issues, advertising technical debugging and tools for Google Publisher Tag.",
            },
            {
                "cluster_key": "creatividades",
                "title": "QA y preview",
                "summary": "This group concentrates the validation of creatives, previews of HTML ads and technical reading of tags or pieces before publishing.",
                "problem": "Resolves doubts about dimensions, click path, tracking, external resources, macros, autoplay and behavior of third-party tags.",
                "use_case": "It is convenient to use it when a creative needs advertising technical QA or when you want to review HTML ad previews in a controlled environment.",
            },
            {
                "cluster_key": "tracking",
                "title": "Tracking and operations",
                "summary": "This block focuses on operational URLs, UTM tagging and final link control before activating traffic or sharing a landing page.",
                "problem": "Helps avoid broken UTMs, inconsistent naming, and manual errors in the final URL that affect measurement and traceability.",
                "use_case": "It is convenient to use it when the problem is not in the creativity or in GPT, but in the construction of the URL that is going to circulate in the media or reporting.",
            },
            {
                "cluster_key": "seo-performance",
                "title": "Performance and technical validation",
                "summary": "This group is used to review the visible technical basis of a landing page or public URL before launching campaigns or attributing the problem to the advertising layer.",
                "problem": "Resolves cases where metadata, canonical, HTML hierarchy or a consistent base response are missing, and where it is advisable to validate the technical status of the page.",
                "use_case": "It is convenient to use it when you need to review a landing page before campaigns, validate visible technical SEO or confirm that the final URL responds as you expect.",
            },
        ],
        "faqs": [
            {
                "question": "What tools does this Pi Development hub page include?",
                "answer": "It includes tools for advertising diagnosis, creative validation, HTML ad preview, advertising technical QA, technical audit of landing pages and construction of UTMs.",
            },
            {
                "question": "Who is this technical suite for?",
                "answer": "It is used for AdOps profiles, trafficking, technical QA, media, monetization, growth and teams that need to review a URL, a creative or an advertising implementation with more technical criteria.",
            },
            {
                "question": "When is it appropriate to use preview, QA or page debug?",
                "answer": "Preview and QA are convenient when the focus is on the part or the tag. The page debug is useful when the problem seems to live in GPT, in the visible monetization or in the implementation of the site.",
            },
            {
                "question": "Do these tools replace DevTools, GAM or manual QA?",
                "answer": "No. They function as a quick and structured review layer to reach the manual review with a better defined technical hypothesis.",
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
