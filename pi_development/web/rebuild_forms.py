from django import forms


PROJECT_TYPE_CHOICES = (
    ("software-system", "Software system"),
    ("mvp", "MVP"),
    ("ai-or-automation", "AI or automation"),
    ("internal-tool", "Internal tool"),
    ("adtech-solution", "AdTech solution"),
    ("technical-research", "Technical research"),
    ("product-collaboration", "Product collaboration"),
    ("other", "Other"),
)


class RebuildContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=120)
    email = forms.EmailField(label="Email", max_length=254)
    company = forms.CharField(label="Company or organization", max_length=160)
    role = forms.CharField(label="Role", max_length=120)
    project_type = forms.ChoiceField(label="Project type", choices=PROJECT_TYPE_CHOICES)
    problem = forms.CharField(
        label="Problem or opportunity",
        widget=forms.Textarea(attrs={"rows": 4}),
        max_length=2000,
    )
    current_situation = forms.CharField(
        label="Current situation",
        widget=forms.Textarea(attrs={"rows": 4}),
        max_length=2000,
    )
    desired_outcome = forms.CharField(
        label="Desired outcome",
        widget=forms.Textarea(attrs={"rows": 4}),
        max_length=2000,
    )
    timeline = forms.CharField(label="Timeline", max_length=160)
    budget_range = forms.CharField(label="Budget range", max_length=160)
    relevant_links = forms.CharField(
        label="Relevant links",
        widget=forms.Textarea(attrs={"rows": 3}),
        max_length=2000,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "pi-form-control")
            field.widget.attrs.setdefault("aria-invalid", "false")

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in list(cleaned_data.items()):
            if isinstance(value, str):
                cleaned_data[field_name] = value.strip()
        return cleaned_data
