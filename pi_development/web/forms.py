"""Build-time form definitions for the three browser-only tools."""

from django import forms


URL_WIDGET_ATTRS = {
    "placeholder": "https://example.com",
    "autocomplete": "url",
    "inputmode": "url",
    "spellcheck": "false",
    "autocapitalize": "none",
}
YES_NO_CHOICES = (("yes", "Yes"), ("no", "No"))
FORMAT_TYPE_CHOICES = (
    ("html5", "Display HTML5"),
    ("static", "Static image"),
    ("video", "Video"),
    ("native", "Native / social"),
    ("other", "Other"),
)
DEVICE_TARGET_CHOICES = (("desktop", "Desktop"), ("mobile", "Mobile"), ("both", "Both"))
SOUND_BEHAVIOR_CHOICES = (
    ("none", "No sound"),
    ("user_action", "Sound after user interaction"),
    ("load", "Sound on load"),
)
AUTOPLAY_BEHAVIOR_CHOICES = (
    ("none", "No autoplay"),
    ("muted", "Muted autoplay"),
    ("sound_on", "Autoplay with sound"),
)
SERVING_CONTEXT_CHOICES = (
    ("safeframe", "SafeFrame"),
    ("friendly_iframe", "Friendly iframe"),
    ("unknown", "Not defined"),
)
CREATIVE_INPUT_MODE_CHOICES = (("html", "HTML creative"), ("third_party", "Third-party tag"))
CREATIVE_PREVIEW_TYPE_CHOICES = (
    ("display", "Display"),
    ("third_party", "Third-party tag"),
    ("rich_media", "Rich media"),
    ("other", "Other"),
)


class CreativePreviewLabForm(forms.Form):
    creative_name = forms.CharField(
        label="Creative name",
        max_length=180,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Spring promotion 300x250"}),
        help_text="Optional context for the review.",
    )
    creative_type = forms.ChoiceField(
        label="Creative type", choices=CREATIVE_PREVIEW_TYPE_CHOICES, initial="display"
    )
    width = forms.IntegerField(
        label="Width",
        min_value=1,
        max_value=4000,
        initial=300,
        widget=forms.NumberInput(attrs={"inputmode": "numeric"}),
        help_text="In pixels.",
    )
    height = forms.IntegerField(
        label="Height",
        min_value=1,
        max_value=4000,
        initial=250,
        widget=forms.NumberInput(attrs={"inputmode": "numeric"}),
        help_text="In pixels.",
    )
    input_mode = forms.ChoiceField(
        label="Input mode",
        choices=CREATIVE_INPUT_MODE_CHOICES,
        initial="html",
        help_text="Use HTML creative for direct markup and Third-party tag for wrappers or external tags.",
    )
    code = forms.CharField(
        label="Creative code",
        required=False,
        max_length=50000,
        widget=forms.Textarea(
            attrs={
                "rows": 12,
                "placeholder": '<div class="creative">Paste HTML creative markup or a third-party tag here.</div>',
            }
        ),
        help_text="Paste the complete markup or tag. The preview runs in an isolated sandbox.",
    )
    click_url = forms.CharField(
        label="Click URL",
        required=False,
        max_length=500,
        widget=forms.TextInput(attrs=URL_WIDGET_ATTRS),
        help_text="Optional. Used only as QA context; it does not rewrite the markup.",
    )
    notes = forms.CharField(
        label="Notes",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Brief context about the placement or technical questions."}
        ),
        help_text="Optional operational context for the review.",
    )


class UTMBuilderForm(forms.Form):
    destination_url = forms.CharField(
        label="Destination URL",
        max_length=500,
        widget=forms.TextInput(
            attrs={**URL_WIDGET_ATTRS, "placeholder": "https://www.example.com/landing"}
        ),
        help_text="Existing query parameters are preserved before UTM values are added.",
    )
    utm_source = forms.CharField(
        label="utm_source",
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "google", "spellcheck": "false", "autocapitalize": "none"}),
        help_text="Traffic source, such as google, linkedin or newsletter.",
    )
    utm_medium = forms.CharField(
        label="utm_medium",
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "cpc", "spellcheck": "false", "autocapitalize": "none"}),
        help_text="Channel or medium, such as cpc, email or social.",
    )
    utm_campaign = forms.CharField(
        label="utm_campaign",
        max_length=160,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "q2_launch", "spellcheck": "false", "autocapitalize": "none"}),
        help_text="A consistent campaign or initiative name.",
    )
    utm_term = forms.CharField(
        label="utm_term",
        max_length=160,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "primary_keyword", "spellcheck": "false", "autocapitalize": "none"}),
    )
    utm_content = forms.CharField(
        label="utm_content",
        max_length=160,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "hero_a", "spellcheck": "false", "autocapitalize": "none"}),
    )


class CreativeQAChecklistForm(forms.Form):
    creative_name = forms.CharField(
        label="Creative name",
        max_length=180,
        widget=forms.TextInput(attrs={"placeholder": "Main promotion 728x90"}),
    )
    format_type = forms.ChoiceField(label="Format", choices=FORMAT_TYPE_CHOICES)
    dimensions = forms.CharField(
        label="Dimensions",
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "300x250"}),
    )
    destination_url = forms.CharField(
        label="Destination URL",
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs=URL_WIDGET_ATTRS),
    )
    click_tag_present = forms.ChoiceField(label="Click tag present?", choices=YES_NO_CHOICES)
    tracking_urls_included = forms.ChoiceField(label="Tracking URLs included?", choices=YES_NO_CHOICES)
    weight_kb = forms.IntegerField(
        label="Weight (KB)",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "150", "inputmode": "numeric"}),
    )
    device_target = forms.ChoiceField(label="Target device", choices=DEVICE_TARGET_CHOICES)
    sound_behavior = forms.ChoiceField(label="Sound behavior", choices=SOUND_BEHAVIOR_CHOICES)
    autoplay_behavior = forms.ChoiceField(label="Autoplay behavior", choices=AUTOPLAY_BEHAVIOR_CHOICES)
    serving_context = forms.ChoiceField(label="Serving context", choices=SERVING_CONTEXT_CHOICES)
    extra_notes = forms.CharField(
        label="Additional notes",
        required=False,
        widget=forms.Textarea(
            attrs={"rows": 4, "placeholder": "Implementation notes, exceptions or clarifications."}
        ),
    )
