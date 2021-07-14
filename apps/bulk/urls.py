# Django
from django.urls import path

# Views
from apps.bulk.views import RenderFieldView

urlpatterns = [
    path(
        route="insoles/forms/<slug:app>/<slug:model>/<slug:field>/",
        view=RenderFieldView.as_view(),
        name="insoles_field",
    ),
]
