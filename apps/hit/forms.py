# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission


# Local


# UserCreationForm
from apps.hit.models import Hit


class HitsForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = (
            "target",
            "description",
            "assignee",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
