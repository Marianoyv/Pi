def build_copy_exports(title, summary, findings, recommendation, sections, insight=None):
    cleaned_findings = [item for item in findings if item]
    markdown_sections = []
    summary_text = summary or "No hay resumen disponible."
    findings_text = "\n".join(f"- {item}" for item in cleaned_findings) or "- No hay hallazgos disponibles."

    if insight:
        insight_lines = build_insight_lines(insight)
        markdown_sections.append(("Priorización", insight_lines))
        summary_text = "\n".join(insight_lines[:4] + ([summary] if summary else []))
        findings_text = "\n".join(f"- {item}" for item in insight.get("highlights") or cleaned_findings) or findings_text

    if summary:
        markdown_sections.append(("Resumen", [summary]))

    for heading, items in sections:
        cleaned_items = [item for item in items if item]
        if cleaned_items:
            markdown_sections.append((heading, cleaned_items))

    if recommendation:
        markdown_sections.append(("Recomendación", [recommendation]))

    return [
        {
            "key": "summary",
            "label": "Copiar resumen",
            "success_message": "Resumen copiado.",
            "text": summary_text,
        },
        {
            "key": "findings",
            "label": "Copiar hallazgos",
            "success_message": "Hallazgos copiados.",
            "text": findings_text,
        },
        {
            "key": "markdown",
            "label": "Copiar resumen en Markdown",
            "success_message": "Markdown copiado.",
            "text": build_markdown_summary(title, markdown_sections),
        },
    ]


def build_markdown_summary(title, sections):
    lines = [f"# {title}", ""]
    for heading, items in sections:
        cleaned_items = [item for item in items if item]
        if not cleaned_items:
            continue
        lines.append(f"## {heading}")
        lines.extend(f"- {item}" for item in cleaned_items)
        lines.append("")
    return "\n".join(lines).strip()


def build_insight_lines(insight):
    lines = [
        f"Estado: {insight['status_label']}",
        f"Puntaje: {insight['score']}/100",
        f"Impacto: {insight['impact']}",
        f"Riesgo: {insight['risk']}",
        f"Prioridad: {insight['priority']}",
    ]
    if insight.get("affected_areas"):
        lines.append("Áreas afectadas: " + ", ".join(insight["affected_areas"]))
    if insight.get("summary"):
        lines.append(insight["summary"])
    return lines
