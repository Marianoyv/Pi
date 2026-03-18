STATUS_THRESHOLDS = (
    (85, "Sólido", "good"),
    (65, "Aceptable", "warn"),
    (40, "Riesgoso", "warn"),
    (0, "Bloqueado", "critical"),
)

IMPACT_ORDER = {"Bajo": 0, "Medio": 1, "Alto": 2}
RISK_ORDER = {"Bajo": 0, "Medio": 1, "Alto": 2, "Bloqueante": 3}
PRIORITY_ORDER = {"Informativa": 0, "Monitorear": 1, "Revisar pronto": 2, "Corregir ahora": 3}


def build_insight_issue(detail, *, penalty, impact, risk, priority, areas):
    return {
        "detail": detail,
        "penalty": penalty,
        "impact": impact,
        "risk": risk,
        "priority": priority,
        "areas": list(areas),
    }


def summarize_insight(issues, *, positive_summary, context_label):
    ranked_issues = sorted(issues, key=lambda item: item["penalty"], reverse=True)
    penalty_total = sum(item["penalty"] for item in ranked_issues)
    score = max(0, 100 - penalty_total)
    status_label, tone = derive_status(score, ranked_issues)
    impact = derive_level(ranked_issues, "impact", IMPACT_ORDER, "Bajo")
    risk = derive_level(ranked_issues, "risk", RISK_ORDER, "Bajo")
    priority = derive_level(ranked_issues, "priority", PRIORITY_ORDER, "Informativa")
    affected_areas = unique_preserve_order(
        area for issue in ranked_issues for area in issue.get("areas") or []
    )
    highlights = [issue["detail"] for issue in ranked_issues[:3]]

    summary = (
        positive_summary
        if not ranked_issues
        else build_issue_summary(status_label, ranked_issues, context_label, affected_areas, impact, priority)
    )

    return {
        "score": score,
        "status_label": status_label,
        "tone": tone,
        "impact": impact,
        "risk": risk,
        "priority": priority,
        "affected_areas": affected_areas,
        "summary": summary,
        "issue_count": len(ranked_issues),
        "highlights": highlights,
    }


def derive_status(score, issues):
    if any(issue["risk"] == "Bloqueante" for issue in issues):
        return "Bloqueado", "critical"

    for threshold, label, tone in STATUS_THRESHOLDS:
        if score >= threshold:
            return label, tone
    return "Bloqueado", "critical"


def derive_level(issues, field_name, order_map, fallback):
    if not issues:
        return fallback

    best_value = fallback
    best_rank = order_map.get(fallback, -1)
    for issue in issues:
        current_value = issue.get(field_name, fallback)
        current_rank = order_map.get(current_value, -1)
        if current_rank > best_rank:
            best_value = current_value
            best_rank = current_rank
    return best_value


def build_issue_summary(status_label, issues, context_label, affected_areas, impact, priority):
    lead_issue = issues[0]["detail"]
    area_label = ", ".join(affected_areas[:2]) if affected_areas else context_label

    if status_label == "Bloqueado":
        return f"{lead_issue} El riesgo es alto para {area_label.lower()}. Conviene corregirlo ahora antes de usar este resultado."

    if status_label == "Riesgoso":
        return f"{lead_issue} Impacto {impact.lower()} sobre {area_label.lower()} con prioridad {priority.lower()}."

    return f"{lead_issue} La base actual sigue siendo usable, pero conviene revisar {area_label.lower()} pronto."


def unique_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        normalized = (item or "").strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result
