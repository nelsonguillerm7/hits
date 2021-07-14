"""View to response rendered templates """

from django.apps import apps
from django.forms import modelform_factory
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string

# Django
from django.views.generic import View


class RenderFieldView(View):
    """View to get record filtering by date"""

    http_method_names = [
        "get",
    ]

    def get_form_class(self, **kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        field_name = kwargs.get("field")
        app = apps.get_app_config(app_name)
        model = app.get_model(model_name)
        form_class = modelform_factory(model, fields=(field_name,))
        return form_class

    def get(self, request, *args, **kwargs):
        app_name = kwargs.get("app")
        model_name = kwargs.get("model")
        field_name = kwargs.get("field")

        if not self.request.user.has_perm(f"{app_name}.change_{model_name}"):
            return HttpResponseForbidden()

        form_class = self.get_form_class(**kwargs)
        form = form_class()
        context = {"field": form[field_name]}
        template = render_to_string("insoles/field.html", context=context)
        res = {"template": template}
        return JsonResponse(res, status=200)
