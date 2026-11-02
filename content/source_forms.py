from django import forms

from .models import SourceLink


class SourceLinkForm(forms.ModelForm):
    class Meta:
        model = SourceLink

        fields = [
            "url",
            "title",
            "published_date",
            "note",
        ]

        widgets = {
            "published_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

        labels = {
            "url": "Source URL",
            "title": "Source Title",
            "published_date": "Publication Date",
            "note": "Notes",
        }