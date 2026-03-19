import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


URL_WIDGET_ATTRS = {
    "placeholder": "https://ejemplo.com",
    "autocomplete": "url",
    "inputmode": "url",
    "spellcheck": "false",
    "autocapitalize": "none",
}

YES_NO_CHOICES = (
    ("yes", "Sí"),
    ("no", "No"),
)

FORMAT_TYPE_CHOICES = (
    ("html5", "Display HTML5"),
    ("static", "Imagen estática"),
    ("video", "Video"),
    ("native", "Nativo / social"),
    ("other", "Otro"),
)

DEVICE_TARGET_CHOICES = (
    ("desktop", "Escritorio"),
    ("mobile", "Móvil"),
    ("both", "Ambos"),
)

SOUND_BEHAVIOR_CHOICES = (
    ("none", "Sin sonido"),
    ("user_action", "Sonido por interacción"),
    ("load", "Sonido al cargar"),
)

AUTOPLAY_BEHAVIOR_CHOICES = (
    ("none", "Sin reproducción automática"),
    ("muted", "Reproducción automática en silencio"),
    ("sound_on", "Reproducción automática con sonido"),
)

SERVING_CONTEXT_CHOICES = (
    ("safeframe", "SafeFrame"),
    ("friendly_iframe", "Iframe amigable"),
    ("unknown", "Sin definir"),
)

CREATIVE_INPUT_MODE_CHOICES = (
    ("html", "Creatividad HTML"),
    ("third_party", "Tag de terceros"),
)

CREATIVE_PREVIEW_TYPE_CHOICES = (
    ("display", "Display"),
    ("third_party", "Tag de terceros"),
    ("rich_media", "Rich media"),
    ("other", "Otro"),
)


def normalize_public_url(raw_value, required=True):
    value = (raw_value or "").strip()
    if not value:
        if required:
            raise forms.ValidationError("Ingresa una URL válida con dominio público.")
        return ""

    normalized_value = value
    if not value.startswith(("http://", "https://")):
        normalized_value = f"https://{value}"

    validator = URLValidator(schemes=["http", "https"])
    try:
        validator(normalized_value)
    except ValidationError as exc:
        raise forms.ValidationError("Ingresa una URL válida con dominio público.") from exc

    return normalized_value


def normalize_utm_value(raw_value):
    value = (raw_value or "").strip().lower()
    if not value:
        return ""
    return re.sub(r"\s+", "-", value)


class UrlToolForm(forms.Form):
    url = forms.CharField(
        label="URL a analizar",
        max_length=500,
        widget=forms.TextInput(attrs=URL_WIDGET_ATTRS),
    )

    def clean_url(self):
        return normalize_public_url(self.cleaned_data.get("url"))


class AiAuditorForm(UrlToolForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["url"].label = "URL publica"
        self.fields["url"].help_text = "Usa una URL accesible sin login para obtener una lectura tecnica real."
        self.fields["url"].widget.attrs.update(
            {
                "placeholder": "https://www.tusitio.com/landing",
            }
        )


class AdTechDebugForm(UrlToolForm):
    pass


class LandingPerformanceSnapshotForm(UrlToolForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["url"].label = "URL publica"
        self.fields["url"].help_text = "Ideal para una landing o pagina de campana que quieras revisar rapido."
        self.fields["url"].widget.attrs.update(
            {
                "placeholder": "https://www.tusitio.com/campana",
            }
        )


class CreativePreviewLabForm(forms.Form):
    creative_name = forms.CharField(
        label="Nombre de la pieza",
        max_length=180,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Promoción primavera 300x250"}),
        help_text="Opcional. Sirve para dejar contexto en la revisión.",
    )
    creative_type = forms.ChoiceField(
        label="Tipo de pieza",
        choices=CREATIVE_PREVIEW_TYPE_CHOICES,
        initial="display",
    )
    width = forms.IntegerField(
        label="Ancho",
        min_value=1,
        max_value=4000,
        initial=300,
        widget=forms.NumberInput(attrs={"inputmode": "numeric"}),
        help_text="En píxeles.",
    )
    height = forms.IntegerField(
        label="Alto",
        min_value=1,
        max_value=4000,
        initial=250,
        widget=forms.NumberInput(attrs={"inputmode": "numeric"}),
        help_text="En píxeles.",
    )
    input_mode = forms.ChoiceField(
        label="Modo de entrada",
        choices=CREATIVE_INPUT_MODE_CHOICES,
        initial="html",
        help_text="Usa Creatividad HTML para markup directo y Tag de terceros para wrappers o etiquetas externas.",
    )
    code = forms.CharField(
        label="Código de la pieza",
        required=False,
        max_length=50000,
        widget=forms.Textarea(
            attrs={
                "rows": 12,
                "placeholder": "<div class=\"creative\">Pega aquí una creatividad HTML o un tag de terceros.</div>",
            }
        ),
        help_text="Pega el markup o el tag completo. La vista previa corre dentro de un sandbox aislado.",
    )
    click_url = forms.CharField(
        label="URL de clic",
        required=False,
        max_length=500,
        widget=forms.TextInput(attrs=URL_WIDGET_ATTRS),
        help_text="Opcional. No reescribe el markup; sirve como referencia para QA.",
    )
    notes = forms.CharField(
        label="Notas",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Notas breves sobre el contexto, el placement o dudas técnicas.",
            }
        ),
        help_text="Opcional. Puede ayudarte a dejar contexto operativo para la revisión.",
    )

    def clean_code(self):
        return (self.cleaned_data.get("code") or "").strip()

    def clean_click_url(self):
        return normalize_public_url(self.cleaned_data.get("click_url"), required=False)

    def clean_creative_name(self):
        return (self.cleaned_data.get("creative_name") or "").strip()

    def clean_notes(self):
        return (self.cleaned_data.get("notes") or "").strip()


class UTMBuilderForm(forms.Form):
    destination_url = forms.CharField(
        label="URL de destino",
        max_length=500,
        widget=forms.TextInput(
            attrs={
                **URL_WIDGET_ATTRS,
                "placeholder": "https://www.tusitio.com/landing",
            }
        ),
        help_text="Se preservan query params existentes antes de agregar UTM.",
    )
    utm_source = forms.CharField(
        label="utm_source",
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "google",
                "spellcheck": "false",
                "autocapitalize": "none",
            }
        ),
        help_text="Origen del trafico, por ejemplo google, linkedin o newsletter.",
    )
    utm_medium = forms.CharField(
        label="utm_medium",
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "cpc",
                "spellcheck": "false",
                "autocapitalize": "none",
            }
        ),
        help_text="Canal o tipo de medio, por ejemplo cpc, email o social.",
    )
    utm_campaign = forms.CharField(
        label="utm_campaign",
        max_length=160,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "lanzamiento_q2",
                "spellcheck": "false",
                "autocapitalize": "none",
            }
        ),
        help_text="Nombre consistente de la campana o iniciativa.",
    )
    utm_term = forms.CharField(
        label="utm_term",
        max_length=160,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "keyword_principal",
                "spellcheck": "false",
                "autocapitalize": "none",
            }
        ),
    )
    utm_content = forms.CharField(
        label="utm_content",
        max_length=160,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "hero_a",
                "spellcheck": "false",
                "autocapitalize": "none",
            }
        ),
    )

    def clean_destination_url(self):
        return normalize_public_url(self.cleaned_data.get("destination_url"))

    def clean(self):
        cleaned_data = super().clean()
        for field_name in (
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "utm_term",
            "utm_content",
        ):
            cleaned_data[field_name] = normalize_utm_value(cleaned_data.get(field_name))
        return cleaned_data


class CreativeQAChecklistForm(forms.Form):
    creative_name = forms.CharField(
        label="Nombre de la pieza",
        max_length=180,
        widget=forms.TextInput(attrs={"placeholder": "Promoción principal 728x90"}),
    )
    format_type = forms.ChoiceField(label="Formato", choices=FORMAT_TYPE_CHOICES)
    dimensions = forms.CharField(
        label="Dimensiones",
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "300x250"}),
    )
    destination_url = forms.CharField(
        label="URL de destino",
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs=URL_WIDGET_ATTRS),
    )
    click_tag_present = forms.ChoiceField(label="¿Tiene click tag?", choices=YES_NO_CHOICES)
    tracking_urls_included = forms.ChoiceField(label="¿Incluye URLs de tracking?", choices=YES_NO_CHOICES)
    weight_kb = forms.IntegerField(
        label="Peso (KB)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "150", "inputmode": "numeric"}),
    )
    device_target = forms.ChoiceField(label="Dispositivo objetivo", choices=DEVICE_TARGET_CHOICES)
    sound_behavior = forms.ChoiceField(label="Comportamiento del sonido", choices=SOUND_BEHAVIOR_CHOICES)
    autoplay_behavior = forms.ChoiceField(label="Reproducción automática", choices=AUTOPLAY_BEHAVIOR_CHOICES)
    serving_context = forms.ChoiceField(label="Contexto de serving", choices=SERVING_CONTEXT_CHOICES)
    extra_notes = forms.CharField(
        label="Notas adicionales",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Notas de implementación, excepciones o aclaraciones.",
            }
        ),
    )

    def clean_dimensions(self):
        value = (self.cleaned_data.get("dimensions") or "").strip()
        if not value:
            return ""
        if not re.fullmatch(r"\d{2,5}\s*[xX]\s*\d{2,5}", value):
            raise forms.ValidationError("Usa un formato de dimensiones válido, por ejemplo 300x250.")
        return re.sub(r"\s+", "", value).lower().replace("x", "x")

    def clean_destination_url(self):
        return normalize_public_url(self.cleaned_data.get("destination_url"), required=False)

    def clean_extra_notes(self):
        return (self.cleaned_data.get("extra_notes") or "").strip()
