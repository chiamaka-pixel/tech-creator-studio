from django import forms

from .models import ContentPerformance


class ContentPerformanceForm(forms.ModelForm):
    class Meta:
        model = ContentPerformance

        fields = [
            "reach",
            "views",
            "likes",
            "comments",
            "shares",
            "notes",
        ]

        labels = {
            "reach": "Reach",
            "views": "Views",
            "likes": "Likes",
            "comments": "Comments",
            "shares": "Shares",
            "notes": "Performance Notes",
        }

        widgets = {
            "reach": forms.NumberInput(attrs={"min": 0}),
            "views": forms.NumberInput(attrs={"min": 0}),
            "likes": forms.NumberInput(attrs={"min": 0}),
            "comments": forms.NumberInput(attrs={"min": 0}),
            "shares": forms.NumberInput(attrs={"min": 0}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }