# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.username = obj.email
        if commit:
            obj.save()
        return obj


class HitmanUpdateForm(forms.ModelForm):
    hitmans = forms.ModelMultipleChoiceField(
        queryset=User.objects.exclude(id=1).filter(
            is_active=True, managers__isnull=True
        ),
        label="Add hitman",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "hitmans",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["readonly"] = True

    def save(self, commit=True):
        obj = super().save(commit=False)
        queryset = self.cleaned_data.get("hitmans")
        for query in queryset:
            query.managers = obj
            query.save()
        obj.save()
        return obj
