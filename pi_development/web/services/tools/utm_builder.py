from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


CORE_UTM_FIELDS = ("utm_source", "utm_medium", "utm_campaign")
OPTIONAL_UTM_FIELDS = ("utm_term", "utm_content")
UTM_FIELDS = CORE_UTM_FIELDS + OPTIONAL_UTM_FIELDS


def run_utm_builder(cleaned_data):
    destination_url = cleaned_data["destination_url"]
    split_url = urlsplit(destination_url)
    existing_pairs = parse_qsl(split_url.query, keep_blank_values=True)

    provided_params = {
        key: cleaned_data.get(key, "")
        for key in UTM_FIELDS
        if cleaned_data.get(key)
    }
    preserved_pairs = [(key, value) for key, value in existing_pairs if key not in provided_params]
    final_pairs = preserved_pairs + [(key, value) for key, value in provided_params.items()]
    final_query = urlencode(final_pairs, doseq=True)
    final_url = urlunsplit(
        (
            split_url.scheme,
            split_url.netloc,
            split_url.path,
            final_query,
            split_url.fragment,
        )
    )

    final_param_map = {key: value for key, value in final_pairs}
    missing_core_fields = [field for field in CORE_UTM_FIELDS if not final_param_map.get(field)]
    existing_utm_pairs = [(key, value) for key, value in existing_pairs if key.startswith("utm_")]
    preserved_non_utm_pairs = [(key, value) for key, value in preserved_pairs if not key.startswith("utm_")]

    overview = build_overview(missing_core_fields, provided_params)
    parameter_rows = build_parameter_rows(cleaned_data, final_param_map, missing_core_fields)
    observations = build_observations(
        missing_core_fields,
        existing_utm_pairs,
        preserved_non_utm_pairs,
        provided_params,
        destination_url,
    )
    recommendation = build_recommendation(missing_core_fields, provided_params, preserved_non_utm_pairs)

    return {
        "target_url": destination_url,
        "final_url": final_url,
        "overview": overview,
        "parameters": parameter_rows,
        "observations": observations,
        "recommendation": recommendation,
        "existing_query_params": preserved_non_utm_pairs,
        "provided_params": provided_params,
    }


def build_overview(missing_core_fields, provided_params):
    if not missing_core_fields and len(provided_params) == 0:
        return {
            "label": "URL ya etiquetada",
            "tone": "good",
            "summary": "La URL base ya traía los parámetros UTM centrales. La herramienta la reconstruyó sin romper la query y dejó la salida lista para copiar.",
        }

    if len(provided_params) == 0:
        return {
            "label": "URL base sin etiquetado nuevo",
            "tone": "warn",
            "summary": "La URL final se puede construir, pero no agregaste nuevos parámetros UTM. La herramienta mantiene la base y deja visible que faltan campos clave.",
        }

    if not missing_core_fields:
        return {
            "label": "URL lista para usar",
            "tone": "good",
            "summary": "La URL final incluye source, medium y campaign. Los parámetros opcionales solo se agregan si los completas.",
        }

    return {
        "label": "URL útil con campos pendientes",
        "tone": "warn",
        "summary": "La URL se construyó correctamente, pero faltan parámetros UTM centrales para dejar el etiquetado más consistente.",
    }


def build_parameter_rows(cleaned_data, final_param_map, missing_core_fields):
    rows = []
    for field in UTM_FIELDS:
        form_value = cleaned_data.get(field, "")
        final_value = final_param_map.get(field, "")
        if form_value:
            status = "ok"
            detail = "Definido en esta corrida."
        elif final_value:
            status = "ok"
            detail = "Tomado desde la URL base."
        elif field in missing_core_fields:
            status = "warn"
            detail = "Falta completar este parámetro base."
        else:
            status = "muted"
            detail = "Opcional en esta versión."
        rows.append(
            {
                "label": field,
                "value": final_value or "No informado",
                "status": status,
                "detail": detail,
            }
        )
    return rows


def build_observations(missing_core_fields, existing_utm_pairs, preserved_non_utm_pairs, provided_params, destination_url):
    observations = []

    if missing_core_fields:
        observations.append(
            "Faltan parámetros base: " + ", ".join(field.replace("utm_", "") for field in missing_core_fields) + "."
        )
    else:
        observations.append("Source, medium y campaign quedaron presentes.")

    if preserved_non_utm_pairs:
        observations.append(
            f"Se preservaron {len(preserved_non_utm_pairs)} query params existentes fuera de UTM."
        )

    if existing_utm_pairs:
        observations.append(
            "La URL original ya tenia UTM. Los campos enviados en el formulario sobrescriben solo las claves completadas."
        )

    if not provided_params:
        observations.append("No se agregaron nuevos parámetros; la salida replica la URL base con sus query params actuales.")

    if "#" in destination_url:
        observations.append("La URL conserva el fragmento original después de reconstruir la query.")

    return observations


def build_recommendation(missing_core_fields, provided_params, preserved_non_utm_pairs):
    if not missing_core_fields and not provided_params:
        return "La URL ya venía con etiquetado base y se reconstruyó sin romper la query original. Conviene revisar si ese naming sigue vigente antes de reutilizarla."

    if not provided_params:
        return "Completa al menos source, medium y campaign antes de usar esta URL en medios o reporting."

    if missing_core_fields:
        first_missing = missing_core_fields[0].replace("utm_", "")
        return (
            f"Completa {first_missing} para cerrar la base del etiquetado. La URL ya está bien formada, pero sin ese campo la lectura analítica queda incompleta."
        )

    if preserved_non_utm_pairs:
        return "La URL final preserva la query original y suma etiquetado consistente. Conviene validar naming antes de compartirla con el equipo."

    return "La URL final ya está lista para copiar y usar. Si el naming cambia por canal, reutiliza esta base y ajusta solo los campos necesarios."
