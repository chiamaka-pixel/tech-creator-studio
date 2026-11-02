from django import forms

from .models import ContentItem


class ContentItemForm(forms.ModelForm):

    class Meta:
        model = ContentItem

        fields = [
            "title",
            "category",
            "audience",
            "content_format",
            "research_notes",
            "draft_text",
            "caption",
            "hashtags",
            "production_notes",
            "planned_date",
            "status",
            "platform",
            "published_url",
        ]

        widgets = {
            "planned_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "research_notes": forms.Textarea(
                attrs={"rows": 4}
            ),
            "draft_text": forms.Textarea(
                attrs={"rows": 6}
            ),
            "caption": forms.Textarea(
                attrs={"rows": 4}
            ),
            "production_notes": forms.Textarea(
                attrs={"rows": 4}
            ),
        }