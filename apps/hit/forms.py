# Django core
from django import forms

# Local apps
from apps.hit.models import Hit


class HitsForm(forms.ModelForm):
    """Class defina model the hits"""

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
