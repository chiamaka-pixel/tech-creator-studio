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
            "title": forms.TextInput(attrs={
                "placeholder": "Give your content a clear, interesting title",
                "autocomplete": "off",
            }),

            "audience": forms.TextInput(attrs={
                "placeholder": "e.g. Beginner tech creators",
            }),

            "research_notes": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Add research, useful facts, references and key points...",
            }),

            "draft_text": forms.Textarea(attrs={
                "rows": 12,
                "placeholder": "Start writing your content here...",
            }),

            "caption": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Write the caption that will accompany your content...",
            }),

            "hashtags": forms.TextInput(attrs={
                "placeholder": "#Tech #AI #SoftwareDevelopment",
            }),

            "production_notes": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Add design instructions, visual ideas or production reminders...",
            }),

            "planned_date": forms.DateInput(attrs={
                "type": "date",
            }),

            "published_url": forms.URLInput(attrs={
                "placeholder": "https://example.com/your-published-content",
            }),
        }