from django import forms


PROJECT_INTENT_CHOICES = (
    ("", "Select the closest starting point"),
    ("build-mvp", "Build an MVP"),
    ("custom-software", "Develop custom software"),
    ("automate-operation", "Automate an operation"),
    ("adtech-solution", "Discuss an AdTech solution"),
    ("improve-platform", "Improve an existing platform"),
    ("other", "Other"),
)


class CompanyContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=120)
    email = forms.EmailField(label="Work email", max_length=254)
    company = forms.CharField(label="Company or team", max_length=160, required=False)
    project_intent = forms.ChoiceField(label="What do you need?", choices=PROJECT_INTENT_CHOICES)
    problem = forms.CharField(
        label="What needs to work better?",
        help_text="A short description of the current situation, user and desired outcome is enough.",
        widget=forms.Textarea(attrs={"rows": 6}),
        max_length=2500,
    )
    relevant_link = forms.URLField(
        label="Relevant URL",
        help_text="Optional: an existing platform, implementation or reference.",
        required=False,
        max_length=500,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "company-form__control")
            field.widget.attrs.setdefault("aria-invalid", "false")

        for field_name, field in self.fields.items():
            if field.help_text:
                field.widget.attrs.setdefault("aria-describedby", f"id_{field_name}_help")

        self.fields["name"].widget.attrs.setdefault("autocomplete", "name")
        self.fields["email"].widget.attrs.setdefault("autocomplete", "email")
        self.fields["company"].widget.attrs.setdefault("autocomplete", "organization")
        self.fields["relevant_link"].widget.attrs.setdefault("placeholder", "https://")

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in list(cleaned_data.items()):
            if isinstance(value, str):
                cleaned_data[field_name] = value.strip()
        return cleaned_data
